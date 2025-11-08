from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import EmotionDiary, EmotionAnalysis, db
from datetime import datetime, timedelta
import json

bp = Blueprint('stats', __name__)

@bp.route('/emotion-trend', methods=['GET'])
@jwt_required()
def get_emotion_trend():
    """获取情绪趋势统计"""
    try:
        user_id = get_jwt_identity()
        days = request.args.get('days', 30, type=int)

        # 计算日期范围
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # 查询日期范围内的分析结果
        analyses = db.session.query(EmotionAnalysis, EmotionDiary).join(
            EmotionDiary, EmotionAnalysis.diary_id == EmotionDiary.id
        ).filter(
            EmotionDiary.user_id == user_id,
            EmotionAnalysis.analyzed_at >= start_date
        ).all()

        # 按日期分组统计
        daily_emotions = {}
        for analysis, diary in analyses:
            date = analysis.analyzed_at.date().isoformat()
            if date not in daily_emotions:
                daily_emotions[date] = {
                    'emotions': [],
                    'intensities': [],
                    'counts': 0
                }

            daily_emotions[date]['emotions'].append(analysis.overall_emotion)
            daily_emotions[date]['intensities'].append(analysis.emotion_intensity)
            daily_emotions[date]['counts'] += 1

        # 计算每日平均情绪
        trend_data = []
        for date, data in daily_emotions.items():
            avg_intensity = sum(data['intensities']) / len(data['intensities']) if data['intensities'] else 0
            most_common_emotion = max(set(data['emotions']), key=data['emotions'].count) if data['emotions'] else 'neutral'

            trend_data.append({
                'date': date,
                'emotion': most_common_emotion,
                'intensity': round(avg_intensity, 2),
                'count': data['counts']
            })

        # 按日期排序
        trend_data.sort(key=lambda x: x['date'])

        return jsonify({
            'trend_data': trend_data,
            'total_days': len(trend_data),
            'period': f'{days} days'
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get emotion trend: {str(e)}'}), 500

@bp.route('/game-progress', methods=['GET'])
@jwt_required()
def get_game_progress_stats():
    """获取游戏进度统计"""
    try:
        user_id = get_jwt_identity()

        # 获取用户的游戏进度
        from models import GameState, GameProgress
        game_state = GameState.query.filter_by(user_id=user_id).first()

        if not game_state:
            return jsonify({'error': 'Game state not found'}), 404

        # 计算各种统计信息
        stats = {
            'current_level': game_state.current_level,
            'game_difficulty': game_state.game_difficulty,
            'total_play_time': game_state.total_play_time,
            'character_stats': game_state.character_stats,
            'unlocked_features_count': len(game_state.unlocked_features),
            'last_active': game_state.last_active.isoformat() if game_state.last_active else None
        }

        # 获取完成的挑战数量
        completed_challenges = GameProgress.query.filter_by(
            user_id=user_id,
            challenge_completed=True
        ).count()

        stats['completed_challenges'] = completed_challenges

        return jsonify({
            'game_stats': stats
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get game progress stats: {str(e)}'}), 500

@bp.route('/cbt-improvement', methods=['GET'])
@jwt_required()
def get_cbt_improvement():
    """获取CBT改善统计"""
    try:
        user_id = get_jwt_identity()

        # 获取用户的所有分析结果
        analyses = db.session.query(EmotionAnalysis, EmotionDiary).join(
            EmotionDiary, EmotionAnalysis.diary_id == EmotionDiary.id
        ).filter(
            EmotionDiary.user_id == user_id,
            EmotionAnalysis.confidence_score > 0.5  # 只考虑置信度较高的分析
        ).order_by(EmotionAnalysis.analyzed_at.desc()).limit(20).all()

        if not analyses:
            return jsonify({'error': 'No analysis data found'}), 404

        # 计算情绪改善指标
        emotion_scores = {
            'happy': 1.0,
            'calm': 0.8,
            'neutral': 0.6,
            'anxious': 0.4,
            'sad': 0.3,
            'angry': 0.2
        }

        recent_scores = []
        for analysis, diary in analyses:
            base_score = emotion_scores.get(analysis.overall_emotion, 0.5)
            weighted_score = base_score * analysis.confidence_score
            recent_scores.append(weighted_score)

        # 计算改善趋势
        if len(recent_scores) >= 2:
            recent_avg = sum(recent_scores[:10]) / min(10, len(recent_scores))
            older_avg = sum(recent_scores[-10:]) / min(10, len(recent_scores))
            improvement_rate = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
        else:
            improvement_rate = 0

        # 统计各种情绪的出现频率
        emotion_frequency = {}
        for analysis, diary in analyses:
            emotion = analysis.overall_emotion
            emotion_frequency[emotion] = emotion_frequency.get(emotion, 0) + 1

        # 计算平均强度
        avg_intensity = sum(analysis.emotion_intensity for analysis, diary in analyses) / len(analyses)

        return jsonify({
            'improvement_rate': round(improvement_rate, 2),
            'emotion_frequency': emotion_frequency,
            'average_intensity': round(avg_intensity, 2),
            'total_analyses': len(analyses),
            'recent_score': recent_scores[0] if recent_scores else 0
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get CBT improvement stats: {str(e)}'}), 500

@bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """获取仪表板综合数据"""
    try:
        user_id = get_jwt_identity()

        # 获取各种统计数据
        from models import User, GameState

        # 用户基本信息
        user = User.query.get(user_id)
        account_age = (datetime.utcnow() - user.created_at).days

        # 日记统计
        total_diaries = EmotionDiary.query.filter_by(user_id=user_id).count()

        # 最近7天的日记数量
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_diaries = EmotionDiary.query.filter(
            EmotionDiary.user_id == user_id,
            EmotionDiary.created_at >= seven_days_ago
        ).count()

        # 游戏统计
        game_state = GameState.query.filter_by(user_id=user_id).first()
        current_level = game_state.current_level if game_state else 1

        # 分析统计
        analysis_count = db.session.query(EmotionAnalysis).join(
            EmotionDiary, EmotionAnalysis.diary_id == EmotionDiary.id
        ).filter(EmotionDiary.user_id == user_id).count()

        # 构建仪表板数据
        dashboard_data = {
            'user_stats': {
                'username': user.username,
                'account_age_days': account_age,
                'is_active': user.is_active
            },
            'diary_stats': {
                'total_diaries': total_diaries,
                'recent_diaries_7d': recent_diaries,
                'avg_diaries_per_week': round(total_diaries / max(1, account_age / 7), 1)
            },
            'game_stats': {
                'current_level': current_level,
                'game_active': bool(game_state)
            },
            'analysis_stats': {
                'total_analyses': analysis_count,
                'analysis_coverage': round((analysis_count / max(1, total_diaries)) * 100, 1) if total_diaries > 0 else 0
            }
        }

        return jsonify({
            'dashboard': dashboard_data,
            'last_updated': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get dashboard data: {str(e)}'}), 500