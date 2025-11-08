// 代码复制功能
function copyCode(button) {
    const codeBlock = button.parentElement;
    const code = codeBlock.querySelector('code').textContent;

    navigator.clipboard.writeText(code).then(() => {
        const originalText = button.textContent;
        button.textContent = '已复制!';
        button.classList.add('copied');

        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('复制失败:', err);
        button.textContent = '复制失败';
        setTimeout(() => {
            button.textContent = '复制';
        }, 2000);
    });
}

// 平滑滚动到锚点
document.addEventListener('DOMContentLoaded', function() {
    // 处理导航链接点击
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // 判断是否是当前页面的锚点链接（以 # 开头，不包含 .html）
            const isCurrentPageAnchor = href.startsWith('#') && !href.includes('.html');

            // 只对当前页面的锚点链接阻止默认行为并添加平滑滚动
            if (isCurrentPageAnchor) {
                e.preventDefault();

                // 移除所有活动状态
                navLinks.forEach(l => l.classList.remove('active'));

                // 添加当前活动状态
                this.classList.add('active');

                // 获取目标区域
                const targetSection = document.querySelector(href);

                if (targetSection) {
                    // 平滑滚动到目标
                    targetSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });

                    // 添加高亮效果
                    targetSection.style.animation = 'none';
                    setTimeout(() => {
                        targetSection.style.animation = 'fadeIn 0.5s ease-out';
                    }, 10);
                }
            }
            // 对于跨页面链接（包含 .html 的链接），让浏览器正常跳转
            // 不需要做任何处理，浏览器会自动跳转
        });
    });

    // 监听滚动，自动更新导航状态
    const sections = document.querySelectorAll('.content-section');
    const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -70% 0px',
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                const correspondingLink = document.querySelector(`a[href="#${id}"]`);

                if (correspondingLink) {
                    navLinks.forEach(link => link.classList.remove('active'));
                    correspondingLink.classList.add('active');
                }
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });

    // 为所有步骤添加进入动画
    const steps = document.querySelectorAll('.step');
    const stepObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateX(-20px)';
                entry.target.style.transition = 'all 0.5s ease-out';

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateX(0)';
                }, 100);

                stepObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    steps.forEach(step => {
        stepObserver.observe(step);
    });

    // 添加键盘快捷键支持
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K 聚焦到第一个导航项
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const firstLink = document.querySelector('.nav-link');
            if (firstLink) firstLink.focus();
        }
    });

    // 代码块增强：点击代码块也可以复制
    document.querySelectorAll('.code-block').forEach(block => {
        const pre = block.querySelector('pre');
        if (pre) {
            pre.style.cursor = 'pointer';
            pre.title = '点击复制代码';

            pre.addEventListener('click', function(e) {
                if (e.target.tagName !== 'BUTTON') {
                    const button = block.querySelector('.copy-btn');
                    if (button) {
                        copyCode(button);
                    }
                }
            });
        }
    });

    // 添加返回顶部按钮
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '↑';
    backToTop.className = 'back-to-top';
    backToTop.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        opacity: 0;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
    `;

    document.body.appendChild(backToTop);

    // 显示/隐藏返回顶部按钮
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTop.style.opacity = '1';
            backToTop.style.pointerEvents = 'auto';
        } else {
            backToTop.style.opacity = '0';
            backToTop.style.pointerEvents = 'none';
        }
    });

    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    backToTop.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-3px)';
        this.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.2)';
    });

    backToTop.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    });

    // 添加加载动画
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s';
        document.body.style.opacity = '1';
    }, 100);

    // 链接外部链接在新标签打开
    document.querySelectorAll('a[href^="http"]').forEach(link => {
        if (!link.hasAttribute('target')) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
});

// 添加页面可见性变化处理
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        document.title = '👋 等你回来 - Claude Code 课程';
    } else {
        document.title = 'Claude Code 系列课程 - 第一节：安装环境';
    }
});
