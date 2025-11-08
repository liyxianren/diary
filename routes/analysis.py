from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import EmotionAnalysis, EmotionDiary, db
from datetime import datetime
import requests
import os

bp = Blueprint('analysis', __name__)

class EmotionAnalysisService:
    """情绪分析服务类"""

    def __init__(self):
        self.coze_api_key = os.getenv('COZE_API_KEY')
        self.coze_bot_id = os.getenv('COZE_BOT_ID')
        self.coze_base_url = os.getenv('COZE_BASE_URL', 'https://api.coze.com')
        self.qwen_api_key = os.getenv('QWEN_API_KEY')
        self.qwen_model = os.getenv('QWEN_MODEL_NAME', 'qwen-turbo')

    def analyze_with_coze(self, text):
        """使用COZE API进行情绪分析"""
        if not self.coze_api_key or not self.coze_bot_id:
            return None

        try:
            # 构建请求数据
            headers = {
                'Authorization': f'Bearer {self.coze_api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                'bot_id': self.coze_bot_id,
                'user_id': 'cbt_diary_user',
                'query': f"请分析以下文本的情绪：{text}",
                'stream': False
            }

            response = requests.post(
                f'{self.coze_base_url}/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return self.parse_coze_response(result)
            else:
                print(f"COZE API调用失败: {response.status_code}")
                return None

        except Exception as e:
            print(f"COZE API调用异常: {str(e)}")
            return None

    def analyze_with_qwen(self, text):
        """使用QWEN模型进行情绪分析"""
        if not self.qwen_api_key:
            return None

        try:
            headers = {
                'Authorization': f'Bearer {self.qwen_api_key}',
                'Content-Type': 'application/json'
            }

            # 构建情绪分析提示词
            prompt = f"""
            请对以下文本进行情绪分析，返回JSON格式的结果：

            文本内容："{text}"

            请分析以下内容并返回JSON格式：
            {{
                "overall_emotion": "主要情绪（happy, sad, angry, anxious, calm, neutral等）",
                "emotion_intensity": 情绪强度（0.0-1.0）,
                "emotion_dimensions": {{
                    "valence": 情绪效价（-1.0到1.0，负值表示负面情绪，正值表示正面情绪）,
                    "arousal": 唤醒度（0.0-1.0，表示情绪的激烈程度）,
                    "dominance": 控制度（0.0-1.0，表示对情绪的控制感）
                }},
                "key_words": ["关键词1", "关键词2", ...],
                "confidence_score": 置信度（0.0-1.0）
            }}
            """

            payload = {
                'model': self.qwen_model,
                'input': {
                    'messages': [
                        {
                            'role': 'system',
                            'content': '你是一个专业的情绪分析助手，请准确分析文本中的情绪状态。'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                },
                'parameters': {
                    'result_format': 'message'
                }
            }

            response = requests.post(
                'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generate',
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return self.parse_qwen_response(result)
            else:
                print(f"QWEN API调用失败: {response.status_code}")
                return None

        except Exception as e:
            print(f"QWEN API调用异常: {str(e)}")
            return None

    def parse_coze_response(self, response_data):
        """解析COZE API响应"""
        try:
            # 这里需要根据COZE API的实际响应格式进行解析
            # 假设返回的是文本格式的情绪分析结果
            content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')

            # 简单的情绪识别逻辑
            emotions = {
                'happy': ['开心', '快乐', '高兴', '愉快', '满足'],
                'sad': ['难过', '悲伤', '沮丧', '失落', '痛苦'],
                'angry': ['生气', '愤怒', '恼火', '气愤', '暴躁'],
                'anxious': ['焦虑', '担心', '紧张', '不安', '恐惧'],
                'calm': ['平静', '宁静', '安详', '放松', '舒适']
            }

            detected_emotion = 'neutral'
            confidence = 0.5

            for emotion, keywords in emotions.items():
                for keyword in keywords:
                    if keyword in content:
                        detected_emotion = emotion
                        confidence = 0.7
                        break

            return {
                'overall_emotion': detected_emotion,
                'emotion_intensity': 0.6,
                'emotion_dimensions': {
                    'valence': 0.0,
                    'arousal': 0.5,
                    'dominance': 0.5
                },
                'key_words': self.extract_keywords(content),
                'confidence_score': confidence
            }

        except Exception as e:
            print(f"COZE响应解析失败: {str(e)}")
            return None

    def parse_qwen_response(self, response_data):
        """解析QWEN API响应"""
        try:
            content = response_data.get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', '')

            # 尝试解析JSON格式
            import json
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                # 如果无法解析JSON，使用备用解析方法
                return self.parse_text_emotion(content)

        except Exception as e:
            print(f"QWEN响应解析失败: {str(e)}")
            return None

    def parse_text_emotion(self, text):
        """从文本中解析情绪信息"""
        emotions = {
            'happy': ['开心', '快乐', '高兴', '愉快', '满足', '幸福'],
            'sad': ['难过', '悲伤', '沮丧', '失落', '痛苦', '伤心'],
            'angry': ['生气', '愤怒', '恼火', '气愤', '暴躁', '气愤'],
            'anxious': ['焦虑', '担心', '紧张', '不安', '恐惧', '害怕'],
            'calm': ['平静', '宁静', '安详', '放松', '舒适', '安心']
        }

        # 简单的情绪识别
        emotion_scores = {}
        for emotion, keywords in emotions.items():
            score = sum(1 for keyword in keywords if keyword in text)
            emotion_scores[emotion] = score

        # 找出得分最高的情绪
        max_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        detected_emotion = max_emotion[0] if max_emotion[1] > 0 else 'neutral'

        return {
            'overall_emotion': detected_emotion,
            'emotion_intensity': min(0.9, max_emotion[1] * 0.3),
            'emotion_dimensions': {
                'valence': 0.0,
                'arousal': 0.5,
                'dominance': 0.5
            },
            'key_words': self.extract_keywords(text),
            'confidence_score': min(0.9, max_emotion[1] * 0.2 + 0.3)
        }

    def extract_keywords(self, text):
        """提取关键词"""
        # 简单的关键词提取
        common_words = ['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这']

        import re
        words = re.findall(r'[\u4e00-\u9fff]+', text)
        word_freq = {}

        for word in words:
            if len(word) >= 2 and word not in common_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # 返回频率最高的前10个词
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:10]]

    def generate_emotion_mapping(self, emotion_data):
        """生成情绪-游戏映射配置"""
        emotion = emotion_data.get('overall_emotion', 'neutral')
        intensity = emotion_data.get('emotion_intensity', 0.5)

        # 游戏难度映射
        difficulty_mapping = {
            'happy': 0.7,
            'sad': 1.2,
            'angry': 1.4,
            'anxious': 1.3,
            'calm': 0.8,
            'neutral': 1.0
        }

        base_difficulty = difficulty_mapping.get(emotion, 1.0)
        final_difficulty = base_difficulty * (0.8 + intensity * 0.4)

        # 角色属性影响
        character_effects = {
            'speed': 1.0,
            'strength': 1.0,
            'intelligence': 1.0
        }

        if emotion == 'sad':
            character_effects['speed'] = 0.8
            character_effects['strength'] = 0.9
        elif emotion == 'angry':
            character_effects['strength'] = 1.2
            character_effects['intelligence'] = 0.9
        elif emotion == 'anxious':
            character_effects['speed'] = 1.1
            character_effects['intelligence'] = 0.8
        elif emotion == 'happy':
            character_effects['speed'] = 1.1
            character_effects['intelligence'] = 1.1

        return {
            'difficulty_modifier': final_difficulty,
            'character_effects': character_effects,
            'scenario_recommendations': self.get_scenario_recommendations(emotion),
            'cbt_challenges': self.generate_cbt_challenges(emotion)
        }

    def get_scenario_recommendations(self, emotion):
        """根据情绪推荐游戏场景"""
        scenarios = {
            'happy': ['阳光草原', '彩虹山谷', '欢乐城堡'],
            'sad': ['宁静湖泊', '月光森林', '温暖小屋'],
            'angry': ['平静海岸', '禅意花园', '冥想空间'],
            'anxious': ['轻松海滩', '舒缓温泉', '安静图书馆'],
            'calm': ['禅意庭院', '平静湖面', '和谐花园']
        }

        return scenarios.get(emotion, ['神秘岛屿'])

    def generate_cbt_challenges(self, emotion):
        """生成CBT挑战任务"""
        challenges = {
            'sad': [
                '识别负面思维模式',
                '寻找积极证据',
                '重构消极想法',
                '练习感恩日记'
            ],
            'angry': [
                '情绪识别练习',
                '愤怒管理技巧',
                '换位思考练习',
                '放松训练'
            ],
            'anxious': [
                '焦虑源识别',
                '现实性检验',
                '应对策略制定',
                '正念练习'
            ],
            'happy': [
                '维持积极状态',
                '分享快乐经验',
                '建立健康习惯',
                '目标设定'
            ],
            'calm': [
                '保持内心平静',
                '深度思考练习',
                '自我反思',
                '持续成长'
            ]
        }

        return challenges.get(emotion, ['基础认知训练'])

# 初始化情绪分析服务
emotion_service = EmotionAnalysisService()

@bp.route('/<int:diary_id>', methods=['POST'])
@jwt_required()
def analyze_diary(diary_id):
    """分析单篇日记的情绪"""
    try:
        user_id = get_jwt_identity()

        # 验证日记所有权
        diary = EmotionDiary.query.filter_by(id=diary_id, user_id=user_id).first()
        if not diary:
            return jsonify({'error': 'Diary not found'}), 404

        # 检查是否已有分析结果
        existing_analysis = EmotionAnalysis.query.filter_by(diary_id=diary_id).first()
        if existing_analysis:
            return jsonify({
                'message': 'Analysis already exists',
                'analysis': existing_analysis.to_dict()
            }), 200

        # 进行情绪分析
        text_content = diary.content

        # 尝试使用COZE API
        coze_result = emotion_service.analyze_with_coze(text_content)

        # 如果COZE失败，使用QWEN
        if coze_result:
            analysis_result = coze_result
            ai_model_version = 'coze'
        else:
            qwen_result = emotion_service.analyze_with_qwen(text_content)
            if qwen_result:
                analysis_result = qwen_result
                ai_model_version = 'qwen'
            else:
                # 如果都失败，使用备用分析
                analysis_result = emotion_service.parse_text_emotion(text_content)
                ai_model_version = 'fallback'

        if not analysis_result:
            return jsonify({'error': 'Failed to analyze emotion'}), 500

        # 创建分析记录
        analysis = EmotionAnalysis(
            diary_id=diary_id,
            overall_emotion=analysis_result.get('overall_emotion', 'neutral'),
            emotion_intensity=analysis_result.get('emotion_intensity', 0.5),
            emotion_dimensions=analysis_result.get('emotion_dimensions', {}),
            key_words=analysis_result.get('key_words', []),
            confidence_score=analysis_result.get('confidence_score', 0.5),
            ai_model_version=ai_model_version
        )

        db.session.add(analysis)

        # 更新日记的分析状态
        diary.analysis_status = 'completed'
        diary.emotion_score = {
            'overall_emotion': analysis_result.get('overall_emotion', 'neutral'),
            'emotion_intensity': analysis_result.get('emotion_intensity', 0.5),
            'confidence_score': analysis_result.get('confidence_score', 0.5)
        }

        db.session.commit()

        # 生成游戏映射配置
        game_mapping = emotion_service.generate_emotion_mapping(analysis_result)

        return jsonify({
            'message': 'Emotion analysis completed',
            'analysis': analysis.to_dict(),
            'game_mapping': game_mapping
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@bp.route('/batch', methods=['POST'])
@jwt_required()
def batch_analyze():
    """批量分析日记"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        diary_ids = data.get('diary_ids', [])
        if not diary_ids:
            return jsonify({'error': 'No diary IDs provided'}), 400

        results = []
        for diary_id in diary_ids:
            # 验证日记所有权
            diary = EmotionDiary.query.filter_by(id=diary_id, user_id=user_id).first()
            if not diary:
                results.append({'diary_id': diary_id, 'status': 'not_found'})
                continue

            # 检查是否已有分析结果
            existing_analysis = EmotionAnalysis.query.filter_by(diary_id=diary_id).first()
            if existing_analysis:
                results.append({
                    'diary_id': diary_id,
                    'status': 'already_analyzed',
                    'analysis': existing_analysis.to_dict()
                })
                continue

            # 进行情绪分析（简化版，实际项目中可以优化为异步处理）
            text_content = diary.content
            analysis_result = emotion_service.analyze_with_coze(text_content)

            if not analysis_result:
                analysis_result = emotion_service.analyze_with_qwen(text_content)

            if not analysis_result:
                analysis_result = emotion_service.parse_text_emotion(text_content)

            if analysis_result:
                # 创建分析记录
                analysis = EmotionAnalysis(
                    diary_id=diary_id,
                    overall_emotion=analysis_result.get('overall_emotion', 'neutral'),
                    emotion_intensity=analysis_result.get('emotion_intensity', 0.5),
                    emotion_dimensions=analysis_result.get('emotion_dimensions', {}),
                    key_words=analysis_result.get('key_words', []),
                    confidence_score=analysis_result.get('confidence_score', 0.5),
                    ai_model_version='batch_analysis'
                )

                db.session.add(analysis)

                # 更新日记状态
                diary.analysis_status = 'completed'
                diary.emotion_score = {
                    'overall_emotion': analysis_result.get('overall_emotion', 'neutral'),
                    'emotion_intensity': analysis_result.get('emotion_intensity', 0.5),
                    'confidence_score': analysis_result.get('confidence_score', 0.5)
                }

                results.append({
                    'diary_id': diary_id,
                    'status': 'analyzed',
                    'analysis': analysis.to_dict()
                })
            else:
                results.append({'diary_id': diary_id, 'status': 'analysis_failed'})

        db.session.commit()

        return jsonify({
            'message': 'Batch analysis completed',
            'results': results
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Batch analysis failed: {str(e)}'}), 500

@bp.route('/<int:diary_id>', methods=['GET'])
@jwt_required()
def get_analysis(diary_id):
    """获取日记的情绪分析结果"""
    try:
        user_id = get_jwt_identity()

        # 验证日记所有权
        diary = EmotionDiary.query.filter_by(id=diary_id, user_id=user_id).first()
        if not diary:
            return jsonify({'error': 'Diary not found'}), 404

        # 获取分析结果
        analysis = EmotionAnalysis.query.filter_by(diary_id=diary_id).first()

        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404

        return jsonify({
            'analysis': analysis.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get analysis: {str(e)}'}), 500

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_analysis_history():
    """获取用户的情绪分析历史"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)

        # 限制每页数量
        limit = min(limit, 100)

        # 查询用户的分析历史
        query = db.session.query(EmotionAnalysis, EmotionDiary).join(
            EmotionDiary, EmotionAnalysis.diary_id == EmotionDiary.id
        ).filter(
            EmotionDiary.user_id == user_id
        ).order_by(EmotionAnalysis.analyzed_at.desc())

        # 分页
        results = query.paginate(page=page, per_page=limit, error_out=False)

        analysis_list = []
        for analysis, diary in results.items:
            analysis_data = analysis.to_dict()
            analysis_data['diary_content'] = diary.content[:100] + '...' if len(diary.content) > 100 else diary.content
            analysis_list.append(analysis_data)

        return jsonify({
            'analysis_history': analysis_list,
            'pagination': {
                'page': results.page,
                'pages': results.pages,
                'per_page': results.per_page,
                'total': results.total,
                'has_prev': results.has_prev,
                'has_next': results.has_next
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get analysis history: {str(e)}'}), 500