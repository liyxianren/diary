/**
 * CBT探险游戏 - 卡牌战斗版本
 *
 * 游戏规则（类似宝可梦）：
 * - 小橘有5滴血，怪物有3-5滴血
 * - 每回合玩家回答一个CBT问题
 * - 答对：小橘攻击怪物，怪物-1血
 * - 答错：怪物反击小橘，小橘-1血
 * - 怪物血量归零=击败，小橘血量归零=战斗失败
 */

// 全局状态
const state = {
    adventureId: null,
    diaryId: null,
    session: null,
    currentMonsterIndex: 0,   // 当前怪物索引（与题目索引同步）
    currentQuestionIndex: 0,  // 当前问题索引
    selectedOptions: [],
    coinsEarned: 0,
    challengeAnswered: false,
    postcardId: null,
    // 战斗系统状态
    xiaojuHp: 5,
    xiaojuMaxHp: 5,
    monsterHp: 1,
    monsterMaxHp: 1,
    monstersDefeated: 0,
    isAnimating: false,
    battleLog: []
};

// Token获取（兼容多种存储方式）
const token = localStorage.getItem('token') || localStorage.getItem('access_token') || sessionStorage.getItem('access_token');

// 怪物图标映射
const MONSTER_ICONS = {
    'dark_cloud': '🌑', 'checkerboard': '♟️', 'crystal_ball': '🔮',
    'rule_stone': '📜', 'label_monster': '🏷️', 'magnifier': '🔍',
    'blame_magnet': '🧲', 'emotion_heart': '💔', 'gratitude_thief': '🦹',
    'achievement_eraser': '📝', 'joy_fog': '🌫️', 'confidence_shadow': '👤'
};

// 怪物图片映射
const MONSTER_SPRITES = {
    'dark_cloud': '/game/monster_dark_cloud.svg',
    'checkerboard': '/game/monster_checkerboard.svg',
    'crystal_ball': '/game/monster_crystal_ball.svg',
    'rule_stone': '/game/monster_rule_stone.svg',
    'label_monster': '/game/monster_label.svg',
    'magnifier': '/game/monster_magnifier.svg',
    'blame_magnet': '/game/monster_blame_magnet.svg',
    'emotion_heart': '/game/monster_emotion_heart.svg',
    'gratitude_thief': '/game/monster_gratitude_thief.svg',
    'achievement_eraser': '/game/monster_achievement_eraser.svg',
    'joy_fog': '/game/monster_joy_fog.svg',
    'confidence_shadow': '/game/monster_confidence_shadow.svg'
};

// 挑战类型名称
const CHALLENGE_TYPE_NAMES = {
    'evidence': '证据收集',
    'reframe': '思维重构'
};

function getActiveMonsterIndex() {
    const monsters = state.session?.monsters || [];
    if (!monsters.length) return 0;
    return Math.min(state.currentQuestionIndex, monsters.length - 1);
}

/**
 * 初始化探险
 */
async function initAdventure(diaryId) {
    state.diaryId = diaryId;

    if (!token) {
        alert('请先登录');
        window.location.href = '/login';
        return;
    }

    const loadingMessages = [
        '小橘正在穿上探险装备...',
        '迷雾森林正在生成中...',
        '小怪物们正在准备...',
        '魔法题目正在酝酿...',
        '小橘正在热身运动...'
    ];
    let messageIndex = 0;
    showLoading(loadingMessages[0]);

    const loadingInterval = setInterval(() => {
        messageIndex = (messageIndex + 1) % loadingMessages.length;
        updateLoadingText(loadingMessages[messageIndex]);
    }, 2000);

    // 轮询获取探险会话（支持后台预生成）
    const maxRetries = 20;  // 最多等待40秒
    let retryCount = 0;

    async function fetchSession() {
        try {
            const response = await fetch(`/api/adventure/session/${diaryId}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || '获取探险会话失败');
            }

            const data = await response.json();

            // 如果还在生成中，继续等待
            if (data.status === 'generating') {
                retryCount++;
                console.log(`[探险] 正在生成中...第 ${retryCount} 次检查`);

                if (retryCount >= maxRetries) {
                    throw new Error('探险生成超时，请稍后重试');
                }

                // 2秒后重试
                setTimeout(fetchSession, 2000);
                return;
            }

            // 生成完成或已存在
            clearInterval(loadingInterval);

            state.session = data;
            state.adventureId = data.id;

            // 恢复战斗状态（如果有）
            if (data.battle_state) {
                state.xiaojuHp = data.battle_state.xiaoju_hp || 5;
                state.currentMonsterIndex = data.battle_state.current_monster || 0;
                state.monstersDefeated = data.battle_state.monsters_defeated || 0;
            }

            hideLoading();

            if (data.status === 'completed') {
                window.location.href = `/postcards`;
            } else if (data.status === 'skipped') {
                window.location.href = `/postcards`;
            } else if (data.status === 'in_progress') {
                state.currentQuestionIndex = data.current_challenge || 0;
                initBattleUI();
                showBattle();
            } else {
                showIntroPanel();
            }

        } catch (error) {
            clearInterval(loadingInterval);
            console.error('初始化探险失败:', error);
            hideLoading();
            alert('加载失败: ' + error.message);
            window.location.href = `/diary/${diaryId}/result`;
        }
    }

    // 开始获取
    fetchSession();
}

function updateLoadingText(text) {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        const loadingText = overlay.querySelector('.loading-text');
        if (loadingText) loadingText.textContent = text;
    }
}

function showLoading(text) {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = overlay.querySelector('.loading-text');
    loadingText.textContent = text || '加载中...';
    overlay.classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('hidden');
}

/**
 * 显示介绍面板
 */
function showIntroPanel() {
    document.getElementById('introPanel').classList.remove('hidden');
    document.getElementById('challengeWrapper').classList.add('hidden');
    document.getElementById('topUI').style.display = 'none';
    document.getElementById('xiaojuArea').style.display = 'none';

    const session = state.session;
    document.querySelector('.intro-panel h2').textContent = session.scene_name || '迷雾森林探险';

    const preview = document.getElementById('monsterPreview');
    preview.innerHTML = '';

    // 预览所有怪物
    if (session.monsters && session.monsters.length > 0) {
        session.monsters.forEach((monster) => {
            const div = document.createElement('div');
            div.className = 'monster-preview-item';
            div.innerHTML = `
                <div class="monster-preview-icon">${MONSTER_ICONS[monster.type] || '👻'}</div>
                <div class="monster-preview-name">${monster.name_zh}</div>
            `;
            preview.appendChild(div);
        });
    }

    const totalMonsters = (session.monsters || []).length;
    document.getElementById('introText').textContent =
        `小橘在迷雾森林中发现了 ${totalMonsters} 只迷雾怪物。完成全部挑战，逐个击败它们吧！`;
}

/**
 * 开始探险
 */
async function startAdventure() {
    showLoading('正在进入迷雾森林...');

    try {
        const response = await fetch(`/api/adventure/${state.adventureId}/start`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || '开始探险失败');
        }

        const data = await response.json();
        state.session = data;
        state.currentQuestionIndex = 0;
        state.currentMonsterIndex = 0;
        state.xiaojuHp = 5;
        state.monstersDefeated = 0;

        hideLoading();
        initBattleUI();
        showBattle();

    } catch (error) {
        console.error('开始探险失败:', error);
        hideLoading();
        alert('开始探险失败: ' + error.message);
    }
}

/**
 * 初始化战斗UI
 */
function initBattleUI() {
    document.getElementById('introPanel').classList.add('hidden');
    document.getElementById('challengeWrapper').classList.remove('hidden');
    document.getElementById('topUI').style.display = 'flex';
    document.getElementById('xiaojuArea').style.display = 'block';

    // 更新小橘血量显示
    updateXiaojuHpDisplay();
}

/**
 * 更新小橘血量显示
 */
function updateXiaojuHpDisplay() {
    const hpBar = document.getElementById('xiaojuHpFill');
    const hpText = document.getElementById('xiaojuHpText');
    if (hpBar) {
        hpBar.style.width = `${(state.xiaojuHp / state.xiaojuMaxHp) * 100}%`;
    }
    if (hpText) {
        hpText.textContent = `${state.xiaojuHp}/${state.xiaojuMaxHp}`;
    }
}

/**
 * 更新怪物血量显示
 */
function updateMonsterHpDisplay() {
    const hpBar = document.getElementById('monsterHpFill');
    const hpText = document.getElementById('monsterHpText');
    if (hpBar) {
        hpBar.style.width = `${(state.monsterHp / state.monsterMaxHp) * 100}%`;
    }
    if (hpText) {
        hpText.textContent = `${state.monsterHp}/${state.monsterMaxHp}`;
    }
}

/**
 * 显示当前战斗
 */
function showBattle() {
    const challenges = state.session.challenges || [];
    const monsters = state.session.monsters || [];
    const challenge = challenges[state.currentQuestionIndex];

    if (!challenge) {
        completeAdventure();
        return;
    }

    // 一个挑战对应一个怪物
    state.currentMonsterIndex = getActiveMonsterIndex();
    const monster = monsters[state.currentMonsterIndex] || monsters[0] || {};

    // 每题一怪：怪物1血，答对即击败
    state.monsterMaxHp = 1;
    state.monsterHp = challenge.completed && challenge.is_correct ? 0 : 1;

    // 重置状态
    state.selectedOptions = [];
    state.challengeAnswered = false;

    // 更新进度
    document.getElementById('challengeProgress').textContent =
        `挑战 ${state.currentQuestionIndex + 1}/${challenges.length}`;
    document.getElementById('coinsEarned').textContent = state.coinsEarned;

    // 更新怪物信息
    document.getElementById('monsterName').textContent = monster.name_zh || '迷雾怪物';

    // 更新怪物图片
    const monsterSprite = document.getElementById('monsterSprite');
    if (monster.type && MONSTER_SPRITES[monster.type]) {
        monsterSprite.style.backgroundImage = `url('${MONSTER_SPRITES[monster.type]}')`;
    } else {
        monsterSprite.style.backgroundImage = "url('/game/monster_dark_cloud.svg')";
    }

    // 更新血量显示
    updateMonsterHpDisplay();
    updateXiaojuHpDisplay();

    // 更新挑战类型徽章
    document.getElementById('challengeTypeBadge').textContent =
        CHALLENGE_TYPE_NAMES[challenge.type] || challenge.type;

    // 更新挑战内容
    document.getElementById('challengeTitle').textContent = challenge.question || '完成这个挑战';
    document.getElementById('distortionThought').textContent =
        challenge.distortion_thought ? `"${challenge.distortion_thought}"` : '';

    // 隐藏空的认知扭曲提示
    const distortionDiv = document.getElementById('distortionThought');
    distortionDiv.style.display = challenge.distortion_thought ? 'block' : 'none';

    // 根据挑战类型显示不同的问题提示
    if (challenge.type === 'evidence') {
        document.getElementById('challengeQuestion').textContent =
            `选出 ${challenge.correct_count || 1} 个正确的选项：`;
    } else {
        document.getElementById('challengeQuestion').textContent =
            '选择一个更平衡、更健康的想法：';
    }

    // 生成选项
    const optionsGrid = document.getElementById('optionsGrid');
    optionsGrid.innerHTML = '';

    challenge.options.forEach((option, index) => {
        const div = document.createElement('div');
        div.className = 'option-item';
        div.dataset.index = index;
        div.onclick = () => toggleOption(index, challenge.type);

        div.innerHTML = `
            <div class="option-checkbox"></div>
            <div class="option-text">${option.text}</div>
        `;

        optionsGrid.appendChild(div);
    });

    // 重置按钮和反馈
    const btnSubmit = document.getElementById('btnSubmit');
    btnSubmit.disabled = true;
    btnSubmit.textContent = '发动攻击！';
    btnSubmit.onclick = submitAnswer;

    document.getElementById('feedbackMessage').className = 'feedback-message';
    document.getElementById('feedbackMessage').textContent = '';
    document.getElementById('cbtInsight').classList.remove('show');

    // 小橘台词
    const speeches = [
        '选对了我就能攻击它！',
        '用智慧击败迷雾怪物！',
        '相信自己的判断！',
        '我们一起加油！'
    ];
    document.getElementById('xiaojuSpeech').textContent =
        speeches[Math.floor(Math.random() * speeches.length)];
}

/**
 * 切换选项选中状态
 */
function toggleOption(index, challengeType) {
    if (state.challengeAnswered || state.isAnimating) return;

    const optionItems = document.querySelectorAll('.option-item');
    const item = optionItems[index];
    const challenge = state.session.challenges[state.currentQuestionIndex];
    const optionId = challenge.options[index].id;

    if (challengeType === 'evidence' && (challenge.correct_count || 1) > 1) {
        // 多选模式
        if (item.classList.contains('selected')) {
            item.classList.remove('selected');
            state.selectedOptions = state.selectedOptions.filter(id => id !== optionId);
        } else {
            item.classList.add('selected');
            state.selectedOptions.push(optionId);
        }
    } else {
        // 单选模式
        optionItems.forEach(el => el.classList.remove('selected'));
        item.classList.add('selected');
        state.selectedOptions = [optionId];
    }

    // 更新提交按钮状态
    const requiredCount = (challengeType === 'evidence' && challenge.correct_count) ? challenge.correct_count : 1;
    document.getElementById('btnSubmit').disabled = state.selectedOptions.length !== requiredCount;
}

/**
 * 提交答案
 */
async function submitAnswer() {
    if (state.challengeAnswered || state.isAnimating) return;

    const challenge = state.session.challenges[state.currentQuestionIndex];
    const currentMonster = (state.session.monsters || [])[getActiveMonsterIndex()] || {};
    const btnSubmit = document.getElementById('btnSubmit');

    btnSubmit.disabled = true;
    btnSubmit.textContent = '判定中...';
    state.isAnimating = true;

    try {
        const response = await fetch(`/api/adventure/${state.adventureId}/submit`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                challenge_index: state.currentQuestionIndex,
                selected_ids: state.selectedOptions
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || '提交失败');
        }

        const result = await response.json();
        state.challengeAnswered = true;

        // 显示正确/错误状态
        const optionItems = document.querySelectorAll('.option-item');
        challenge.options.forEach((option, index) => {
            const item = optionItems[index];
            const optionId = option.id;
            if (result.correct_ids.includes(optionId)) {
                item.classList.add('correct');
            } else if (state.selectedOptions.includes(optionId)) {
                item.classList.add('incorrect');
            }
        });

        // 执行战斗动画
        if (result.correct) {
            await playAttackAnimation('xiaoju', 'monster');
            state.monsterHp = 0;
            updateMonsterHpDisplay();

            state.coinsEarned += result.coins_earned || 10;
            document.getElementById('coinsEarned').textContent = state.coinsEarned;

            await playDefeatAnimation('monster');
            state.monstersDefeated++;
            showBattleMessage(`击败了${currentMonster.name_zh || '迷雾怪物'}！`, 'success');
            document.getElementById('xiaojuSpeech').textContent = '太棒了！我们继续前进！';
        } else {
            await playAttackAnimation('monster', 'xiaoju');
            state.xiaojuHp--;
            updateXiaojuHpDisplay();

            showBattleMessage(`答错了！小橘受到攻击，还剩 ${state.xiaojuHp} 滴血`, 'error');

            // 检查小橘是否被击败
            if (state.xiaojuHp <= 0) {
                await playDefeatAnimation('xiaoju');
                document.getElementById('xiaojuSpeech').textContent = '呜...我倒下了...';
                state.isAnimating = false;
                showGameOver();
                return;
            } else {
                document.getElementById('xiaojuSpeech').textContent = '呜...好痛...下次一定选对！';
            }
        }

        // 显示CBT洞察
        if (result.cbt_insight) {
            document.getElementById('cbtInsightText').textContent = result.cbt_insight;
            document.getElementById('cbtInsight').classList.add('show');
        }

        state.isAnimating = false;

        // 更新按钮
        const nextIndex = typeof result.next_challenge === 'number'
            ? result.next_challenge
            : state.currentQuestionIndex + 1;
        const hasNextChallenge = !result.is_last && nextIndex < (state.session.challenges || []).length;

        if (state.xiaojuHp <= 0) {
            btnSubmit.textContent = '探险结束';
            btnSubmit.onclick = showGameOver;
        } else if (hasNextChallenge) {
            btnSubmit.textContent = '继续战斗';
            btnSubmit.onclick = () => {
                state.currentQuestionIndex = nextIndex;
                showBattle();
            };
        } else {
            btnSubmit.textContent = '完成探险';
            btnSubmit.onclick = completeAdventure;
        }
        btnSubmit.disabled = false;

    } catch (error) {
        console.error('提交答案失败:', error);
        btnSubmit.textContent = '发动攻击！';
        btnSubmit.disabled = false;
        state.isAnimating = false;
        alert('提交失败: ' + error.message);
    }
}

/**
 * 播放攻击动画
 */
async function playAttackAnimation(attacker, target) {
    return new Promise(resolve => {
        const attackerEl = attacker === 'xiaoju'
            ? document.querySelector('.xiaoju-sprite')
            : document.getElementById('monsterSprite');
        const targetEl = target === 'xiaoju'
            ? document.querySelector('.xiaoju-sprite')
            : document.getElementById('monsterSprite');

        if (!attackerEl || !targetEl) {
            resolve();
            return;
        }

        // 添加攻击者冲刺动画
        attackerEl.classList.add('attack-dash');

        // 播放攻击音效（如果有）
        playSound('attack');

        setTimeout(() => {
            // 攻击者恢复
            attackerEl.classList.remove('attack-dash');

            // 目标受击动画
            targetEl.classList.add('hit-shake');

            // 显示伤害数字
            showDamageNumber(target, '-1');

            // 播放受击音效
            playSound('hit');

            setTimeout(() => {
                targetEl.classList.remove('hit-shake');
                resolve();
            }, 400);
        }, 300);
    });
}

/**
 * 播放击败动画
 */
async function playDefeatAnimation(who) {
    return new Promise(resolve => {
        const el = who === 'xiaoju'
            ? document.querySelector('.xiaoju-sprite')
            : document.getElementById('monsterSprite');

        if (!el) {
            resolve();
            return;
        }

        el.classList.add('defeat-fade');
        playSound('defeat');

        setTimeout(() => {
            el.classList.remove('defeat-fade');
            resolve();
        }, 800);
    });
}

/**
 * 显示伤害数字
 */
function showDamageNumber(target, text) {
    const container = target === 'xiaoju'
        ? document.getElementById('xiaojuArea')
        : document.getElementById('monsterArea');

    if (!container) return;

    const dmgEl = document.createElement('div');
    dmgEl.className = 'damage-number';
    dmgEl.textContent = text;
    container.appendChild(dmgEl);

    setTimeout(() => {
        dmgEl.remove();
    }, 1000);
}

/**
 * 播放音效
 */
function playSound(type) {
    // 可以在这里添加音效播放逻辑
    // 目前只是占位符
    console.log(`[Sound] ${type}`);
}

/**
 * 显示战斗消息
 */
function showBattleMessage(message, type) {
    const feedback = document.getElementById('feedbackMessage');
    feedback.className = `feedback-message ${type}`;
    feedback.innerHTML = `<i class="fas fa-${type === 'success' ? 'check' : 'times'}-circle"></i> ${message}`;
}

/**
 * 显示游戏结束
 */
function showGameOver() {
    const modal = document.getElementById('victoryModal');
    const content = modal.querySelector('.victory-content');

    content.innerHTML = `
        <div class="victory-icon">😢</div>
        <h2 class="victory-title">探险失败</h2>
        <p class="victory-subtitle">小橘被迷雾怪物击败了...</p>
        <div class="rewards-list">
            <div class="reward-item">
                <span class="reward-label"><i class="fas fa-skull" style="color: #666;"></i> 击败怪物</span>
                <span class="reward-value">${state.monstersDefeated}</span>
            </div>
            <div class="reward-item">
                <span class="reward-label"><i class="fas fa-coins" style="color: #ffd700;"></i> 获得金币</span>
                <span class="reward-value">+${Math.floor(state.coinsEarned / 2)}</span>
            </div>
        </div>
        <p style="color: #666; margin: 20px 0;">别灰心，下次一定能成功！</p>
        <button class="btn-view-postcard" onclick="window.location.href='/diary/${state.diaryId}/result'">
            <i class="fas fa-redo"></i> 返回日记
        </button>
    `;

    modal.classList.add('show');
}

/**
 * 完成探险
 */
async function completeAdventure() {
    showLoading('正在结算奖励...');

    try {
        const response = await fetch(`/api/adventure/${state.adventureId}/complete`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                xiaoju_hp: state.xiaojuHp,
                monsters_defeated: state.monstersDefeated
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || '完成探险失败');
        }

        const result = await response.json();
        hideLoading();
        showVictoryModal(result);

    } catch (error) {
        console.error('完成探险失败:', error);
        hideLoading();
        alert('完成探险失败: ' + error.message);
    }
}

/**
 * 显示胜利弹窗
 */
function showVictoryModal(result) {
    const modal = document.getElementById('victoryModal');
    const content = modal.querySelector('.victory-content');

    state.postcardId = result.postcard_id;

    let rewardsHtml = '';

    // 战斗统计
    rewardsHtml += `
        <div class="reward-item">
            <span class="reward-label"><i class="fas fa-heart" style="color: #e74c3c;"></i> 小橘剩余血量</span>
            <span class="reward-value">${state.xiaojuHp}/${state.xiaojuMaxHp}</span>
        </div>
    `;

    // 击败怪物
    rewardsHtml += `
        <div class="reward-item">
            <span class="reward-label"><i class="fas fa-ghost" style="color: #9b59b6;"></i> 击败怪物</span>
            <span class="reward-value">${result.monsters_defeated || state.monstersDefeated}</span>
        </div>
    `;

    // 金币奖励
    if (result.coins_earned > 0) {
        rewardsHtml += `
            <div class="reward-item">
                <span class="reward-label"><i class="fas fa-coins" style="color: #ffd700;"></i> 金币</span>
                <span class="reward-value">+${result.coins_earned}</span>
            </div>
        `;
    }

    // 道具奖励
    if (result.items_earned && result.items_earned.length > 0) {
        result.items_earned.forEach(item => {
            rewardsHtml += `
                <div class="reward-item">
                    <span class="reward-label"><i class="fas fa-gift" style="color: #9b59b6;"></i> ${item.name_zh}</span>
                    <span class="reward-value">+1</span>
                </div>
            `;
        });
    }

    // 属性变化
    if (result.stat_changes) {
        const statNames = {
            'mental_health': '心理健康',
            'stress': '压力值',
            'growth': '成长潜力'
        };

        for (const [stat, change] of Object.entries(result.stat_changes)) {
            if (change !== 0) {
                const isPositive = (stat === 'stress' && change < 0) || (stat !== 'stress' && change > 0);
                rewardsHtml += `
                    <div class="reward-item">
                        <span class="reward-label">
                            <i class="fas fa-heart" style="color: ${isPositive ? '#28a745' : '#dc3545'};"></i>
                            ${statNames[stat] || stat}
                        </span>
                        <span class="reward-value ${isPositive ? '' : 'negative'}">
                            ${change > 0 ? '+' : ''}${change}
                        </span>
                    </div>
                `;
            }
        }
    }

    content.innerHTML = `
        <div class="victory-icon">🎉</div>
        <h2 class="victory-title">探险胜利！</h2>
        <p class="victory-subtitle">小橘成功击败了所有迷雾怪物！</p>
        <div class="rewards-list" id="rewardsList">${rewardsHtml}</div>
        <button class="btn-view-postcard" onclick="viewPostcard()">
            <i class="fas fa-envelope"></i> 查看明信片
        </button>
    `;

    modal.classList.add('show');
}

/**
 * 跳过探险
 */
async function skipAdventure() {
    if (!confirm('确定要跳过探险吗？跳过后将无法获得奖励。')) {
        return;
    }

    showLoading('正在跳过...');

    try {
        const response = await fetch(`/api/adventure/${state.adventureId}/skip`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || '跳过失败');
        }

        hideLoading();
        window.location.href = `/diary/${state.diaryId}/result`;

    } catch (error) {
        console.error('跳过探险失败:', error);
        hideLoading();
        alert('跳过失败: ' + error.message);
    }
}

/**
 * 查看明信片
 */
async function viewPostcard() {
    if (state.postcardId) {
        window.location.href = `/postcard/${state.postcardId}`;
    } else {
        try {
            const response = await fetch(`/api/postcard/by-diary/${state.diaryId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.postcard && data.postcard.id) {
                    window.location.href = `/postcard/${data.postcard.id}`;
                    return;
                }
            }
        } catch (e) {
            console.log('查询明信片失败，跳转到列表页');
        }

        window.location.href = `/postcards`;
    }
}
