from flask import Flask, render_template
import os

app = Flask(__name__)

# 课程配置数据
COURSES_DATA = {
    1: {
        'title': '第一节课：安装环境',
        'link': '/lesson1',
        'sections': [
            {'href': '/lesson1#mac-install', 'text': 'Mac 安装'},
            {'href': '/lesson1#windows-install', 'text': 'Windows 安装'},
            {'href': '/lesson1#chatglm-config', 'text': '转接 ChatGLM'}
        ]
    },
    2: {
        'title': '第二节课：基础使用',
        'link': '/lesson2',
        'sections': [
            {'href': '/lesson2#claude-intro', 'text': 'Claude Code 介绍'},
            {'href': '/lesson2#agent-concept', 'text': 'Agent 概念详解'},
            {'href': '/lesson2#context-retrieval', 'text': '上下文检索机制'},
            {'href': '/lesson2#relay-principle', 'text': '转接原理'},
            {'href': '/lesson2#workspace-switch', 'text': '工作区切换'}
        ]
    },
    3: {
        'title': '第三节课：高级用法',
        'link': '/lesson3',
        'sections': [
            {'href': '/lesson3#claude-md', 'text': 'CLAUDE.md 配置'},
            {'href': '/lesson3#rules-file', 'text': 'rules 规则文件'},
            {'href': '/lesson3#prompt-mastery', 'text': 'Prompt 提示词精通'},
            {'href': '/lesson3#mode-switching', 'text': '模式切换 (Alt+M)'}
        ]
    },
    4: {
        'title': '第四节课：实战项目',
        'link': '/lesson4',
        'sections': [
            {'href': '/lesson4#snake-game', 'text': '项目1：贪吃蛇游戏'},
            {'href': '/lesson4#todo-app', 'text': '项目2：待办事项应用'},
            {'href': '/lesson4#practice-tips', 'text': '实战技巧总结'}
        ]
    },
    5: {
        'title': '第五节课：CBT项目详解',
        'link': '/lesson5',
        'sections': [
            {'href': '/lesson5#project-overview', 'text': '项目概述'},
            {'href': '/lesson5#cbt-theory', 'text': 'CBT理论基础'},
            {'href': '/lesson5#cbt-application', 'text': 'CBT应用实践'},
            {'href': '/lesson5#tech-architecture', 'text': '技术架构'},
            {'href': '/lesson5#game-design', 'text': '游戏化设计'},
            {'href': '/lesson5#discussion', 'text': '小组讨论'},
            {'href': '/lesson5#project-progress', 'text': '项目进展'}
        ]
    },
    6: {
        'title': '第六节课：Claude Code实战',
        'link': '/lesson6',
        'sections': [
            {'href': '/lesson6#practical-goals', 'text': '实战目标'},
            {'href': '/lesson6#development-steps', 'text': '开发步骤'},
            {'href': '/lesson6#claude-tips', 'text': 'Claude技巧'},
            {'href': '/lesson6#quick-commands', 'text': '快速命令'},
            {'href': '/lesson6#common-issues', 'text': '常见问题'},
            {'href': '/lesson6#practice-results', 'text': '实战成果'}
        ]
    }
}

# 主页路由
@app.route('/')
def index():
    return render_template('index.html', courses=COURSES_DATA)

# 课程页面路由
@app.route('/lesson<int:lesson_id>')
def lesson(lesson_id):
    template_map = {
        1: 'lesson1.html',
        2: 'lesson2.html',
        3: 'lesson3.html',
        4: 'lesson4.html',
        5: 'lesson5.html',
        6: 'lesson6.html'
    }

    template_name = template_map.get(lesson_id, '404.html')
    if template_name == '404.html':
        return render_template('404.html'), 404

    return render_template(template_name,
                         courses=COURSES_DATA,
                         current_lesson=lesson_id)

# 404错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500错误处理
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')