from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import EmotionDiary, db, User
from datetime import datetime, timedelta

bp = Blueprint('diary', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_diaries():
    """获取用户的日记列表"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        # 限制每页数量
        limit = min(limit, 50)

        # 查询用户的日记
        query = EmotionDiary.query.filter_by(user_id=user_id).order_by(EmotionDiary.created_at.desc())

        # 分页
        diaries = query.paginate(page=page, per_page=limit, error_out=False)

        return jsonify({
            'diaries': [diary.to_dict() for diary in diaries.items],
            'pagination': {
                'page': diaries.page,
                'pages': diaries.pages,
                'per_page': diaries.per_page,
                'total': diaries.total,
                'has_prev': diaries.has_prev,
                'has_next': diaries.has_next
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get diaries: {str(e)}'}), 500

@bp.route('/recent', methods=['GET'])
def get_recent_diaries():
    """获取最新的日记（公开，用于首页展示）"""
    try:
        # 获取最近10条日记（匿名显示）
        diaries = EmotionDiary.query.order_by(EmotionDiary.created_at.desc()).limit(10).all()

        # 匿名化处理，不显示用户敏感信息
        result = []
        for diary in diaries:
            diary_data = diary.to_dict()
            # 移除内容中的敏感信息，只显示前100个字符
            if len(diary_data['content']) > 100:
                diary_data['content'] = diary_data['content'][:100] + '...'
            result.append(diary_data)

        return jsonify({
            'diaries': result
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get recent diaries: {str(e)}'}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_diary():
    """创建新的日记"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # 验证必填字段
        if not data.get('content') or not data['content'].strip():
            return jsonify({'error': 'Content is required'}), 400

        content = data['content'].strip()
        emotion_tags = data.get('emotion_tags', [])

        # 创建新日记
        new_diary = EmotionDiary(
            user_id=user_id,
            content=content,
            emotion_tags=emotion_tags,
            emotion_score={}
        )

        db.session.add(new_diary)
        db.session.commit()

        return jsonify({
            'message': 'Diary created successfully',
            'diary': new_diary.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create diary: {str(e)}'}), 500

@bp.route('/<int:diary_id>', methods=['GET'])
@jwt_required()
def get_diary(diary_id):
    """获取单篇日记详情"""
    try:
        user_id = get_jwt_identity()

        # 查询日记
        diary = EmotionDiary.query.filter_by(id=diary_id, user_id=user_id).first()

        if not diary:
            return jsonify({'error': 'Diary not found'}), 404

        # 获取关联的分析结果
        diary_data = diary.to_dict()
        if diary.analysis:
            diary_data['analysis'] = diary.analysis.to_dict()

        return jsonify({
            'diary': diary_data
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get diary: {str(e)}'}), 500

@bp.route('/<int:diary_id>', methods=['PUT'])
@jwt_required()
def update_diary(diary_id):
    """更新日记"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # 查询日记
        diary = EmotionDiary.query.filter_by(id=diary_id, user_id=user_id).first()

        if not diary:
            return jsonify({'error': 'Diary not found'}), 404

        # 更新内容
        if 'content' in data:
            content = data['content'].strip()
            if not content:
                return jsonify({'error': 'Content cannot be empty'}), 400
            diary.content = content

        # 更新情绪标签
        if 'emotion_tags' in data:
            diary.emotion_tags = data['emotion_tags']

        # 重置分析状态
        diary.analysis_status = 'pending'
        diary.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'message': 'Diary updated successfully',
            'diary': diary.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update diary: {str(e)}'}), 500

@bp.route('/<int:diary_id>', methods=['DELETE'])
@jwt_required()
def delete_diary(diary_id):
    """删除日记"""
    try:
        user_id = get_jwt_identity()

        # 查询日记
        diary = EmotionDiary.query.filter_by(id=diary_id, user_id=user_id).first()

        if not diary:
            return jsonify({'error': 'Diary not found'}), 404

        # 删除日记
        db.session.delete(diary)
        db.session.commit()

        return jsonify({
            'message': 'Diary deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete diary: {str(e)}'}), 500

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_diary_stats():
    """获取日记统计信息"""
    try:
        user_id = get_jwt_identity()

        # 计算统计信息
        total_diaries = EmotionDiary.query.filter_by(user_id=user_id).count()

        # 最近7天的日记数量
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_diaries = EmotionDiary.query.filter(
            EmotionDiary.user_id == user_id,
            EmotionDiary.created_at >= seven_days_ago
        ).count()

        # 按情绪标签统计
        all_diaries = EmotionDiary.query.filter_by(user_id=user_id).all()
        emotion_stats = {}

        for diary in all_diaries:
            for tag in diary.emotion_tags:
                if tag not in emotion_stats:
                    emotion_stats[tag] = 0
                emotion_stats[tag] += 1

        return jsonify({
            'total_diaries': total_diaries,
            'recent_diaries': recent_diaries,
            'emotion_stats': emotion_stats,
            'avg_diaries_per_week': round(total_diaries / max(1, (datetime.utcnow() - User.query.get(user_id).created_at).days / 7), 2)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get diary stats: {str(e)}'}), 500

@bp.route('/search', methods=['GET'])
@jwt_required()
def search_diaries():
    """搜索日记"""
    try:
        user_id = get_jwt_identity()

        # 获取搜索参数
        keyword = request.args.get('keyword', '').strip()
        emotion_tag = request.args.get('emotion_tag', '').strip()
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')

        # 基础查询
        query = EmotionDiary.query.filter_by(user_id=user_id)

        # 关键词搜索
        if keyword:
            query = query.filter(EmotionDiary.content.contains(keyword))

        # 情绪标签筛选
        if emotion_tag:
            query = query.filter(EmotionDiary.emotion_tags.contains([emotion_tag]))

        # 日期范围筛选
        if date_from:
            try:
                from_date = datetime.fromisoformat(date_from)
                query = query.filter(EmotionDiary.created_at >= from_date)
            except ValueError:
                pass

        if date_to:
            try:
                to_date = datetime.fromisoformat(date_to)
                query = query.filter(EmotionDiary.created_at <= to_date)
            except ValueError:
                pass

        # 执行查询
        diaries = query.order_by(EmotionDiary.created_at.desc()).all()

        return jsonify({
            'diaries': [diary.to_dict() for diary in diaries],
            'total': len(diaries)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to search diaries: {str(e)}'}), 500