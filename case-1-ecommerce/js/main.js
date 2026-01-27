'use strict';

const App = {
    config: {
        animationDuration: 2000,
        chatMinDelay: 300,
        chatMaxDelay: 2000,
        counterStep: 16,
        observerThreshold: 0.3
    },
    
    state: {
        countersAnimated: false,
        chatMessageCount: 0,
        autoSolvedCount: 0
    },

    init() {
        try {
            this.initChat();
            this.initCounters();
            this.initComponentLinks();
            this.initMobileTabs();
            this.initTableInteraction();
            this.initTimelineInteraction();
            this.initScrollAnimations();
            this.initQuickQuestions();
        } catch (error) {
            console.error('[App] Init error:', error);
        }
    },

    chatHistory: [],

    initChat() {
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-btn');
        const chatMessages = document.getElementById('chat-messages');
        const typingIndicator = document.getElementById('typing-indicator');
        
        if (!chatInput || !sendButton || !chatMessages) return;

        const sendMessage = async () => {
            const message = chatInput.value.trim();
            if (!message) return;
            
            this.addChatMessage(message, 'user');
            chatInput.value = '';
            this.showTypingIndicator();
            
            const startTime = Date.now();
            
            try {
                const response = await this.callAI(message);
                this.hideTypingIndicator();
                const responseTime = ((Date.now() - startTime) / 1000).toFixed(1);
                this.addChatMessage(response, 'bot', responseTime);
            } catch (error) {
                this.hideTypingIndicator();
                const fallbackAnswer = this.findAnswer(message);
                const responseTime = ((Date.now() - startTime) / 1000).toFixed(1);
                this.addChatMessage(fallbackAnswer, 'bot', responseTime);
            }
        };

        sendButton.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
    },

    async callAI(message) {
        this.chatHistory.push({ role: 'user', content: message });
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message, 
                history: this.chatHistory.slice(-10) 
            })
        });
        
        if (!response.ok) throw new Error('API error');
        
        const data = await response.json();
        this.chatHistory.push({ role: 'assistant', content: data.reply });
        
        return data.reply;
    },

    initQuickQuestions() {
        const quickButtons = document.querySelectorAll('.quick-question-btn');
        quickButtons.forEach(btn => {
            btn.addEventListener('click', async () => {
                const question = btn.dataset.question;
                if (!question) return;
                this.addChatMessage(question, 'user');
                this.showTypingIndicator();
                const startTime = Date.now();
                
                try {
                    const response = await this.callAI(question);
                    this.hideTypingIndicator();
                    const responseTime = ((Date.now() - startTime) / 1000).toFixed(1);
                    this.addChatMessage(response, 'bot', responseTime);
                } catch (error) {
                    this.hideTypingIndicator();
                    const fallbackAnswer = this.findAnswer(question);
                    const responseTime = ((Date.now() - startTime) / 1000).toFixed(1);
                    this.addChatMessage(fallbackAnswer, 'bot', responseTime);
                }
            });
        });
    },

    addChatMessage(text, type, responseTime = null) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type === 'user' ? 'user-message' : 'bot-message'}`;
        let content = text;
        if (responseTime && type === 'bot') {
            content += `<span class="response-time">Ответ за ${responseTime} сек</span>`;
        }
        messageDiv.innerHTML = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    },

    showTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.classList.remove('hidden');
    },

    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.classList.add('hidden');
    },

    getLocalQuestions() {
        return [
            {
                question: 'тест',
                answer: 'Отлично! Я готов. Спрашивайте про наличие, доставку, возврат или состав товара. Я отвечу мгновенно!',
                keywords: ['тест', 'проверим', 'протестируем', 'работай', 'начали'],
            },
            {
                question: 'привет',
                answer: 'Привет! 👋 Я интеллектуальный ассистент этого магазина. Чем я могу помочь вам сегодня?',
                keywords: ['привет', 'здравствуйте', 'добрый день', 'хай', 'ку'],
            },
            {
                question: 'Есть ли в наличии?',
                answer: 'Да, товар в наличии на основном складе! Осталось более 10 штук. При заказе сегодня — доставка завтра.',
                keywords: ['наличие', 'есть', 'остаток', 'склад', 'купить'],
            },
            {
                question: 'Как вернуть?',
                answer: 'Возврат очень прост: у вас есть 14 дней. Просто принесите товар в любой пункт выдачи Wildberries. Деньги вернутся на карту в течение 1-3 дней.',
                keywords: ['вернуть', 'возврат', 'обмен', 'не подошел'],
            },
            {
                question: 'Стоимость доставки',
                answer: 'Доставка по всей России абсолютно бесплатна для заказов от 500 ₽. Для остальных — фиксированные 200 ₽.',
                keywords: ['доставка', 'стоимость', 'цена', 'бесплатно'],
            },
            {
                question: 'Состав ткани',
                answer: 'Мы используем 100% натуральный хлопок высшего сорта (пенье). Материал гипоаллергенный и очень приятный к телу.',
                keywords: ['состав', 'ткань', 'материал', 'хлопок', 'натуральный'],
            }
        ];
    },

    findAnswer(question) {
        const questions = this.getLocalQuestions();
        const normalized = question.toLowerCase().trim();
        
        const exact = questions.find(q => q.question.toLowerCase() === normalized);
        if (exact) return exact.answer;

        const partial = questions.find(q => {
            const keywords = q.keywords || [];
            return keywords.some(k => normalized.includes(k.toLowerCase()));
        });
        
        if (partial) return partial.answer;

        return 'Я постоянно учусь! Попробуйте спросить про **наличие**, **доставку** или **возврат**. Эти темы я знаю лучше всего.';
    },

    generateRandomDelay() {
        return Math.floor(Math.random() * (1200 - 400 + 1)) + 400;
    },

    initCounters() {
        const section = document.getElementById('kpi-section');
        if (!section) return;
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !this.state.countersAnimated) {
                    this.animateAllCounters();
                    this.state.countersAnimated = true;
                }
            });
        }, { threshold: 0.3 });
        observer.observe(section);
    },

    animateAllCounters() {
        const counters = document.querySelectorAll('.animated-counter');
        counters.forEach((counter, index) => {
            const target = parseFloat(counter.dataset.target) || 0;
            const suffix = counter.dataset.suffix || '';
            const decimal = parseInt(counter.dataset.decimal) || 0;
            counter.textContent = '0' + suffix;
            setTimeout(() => {
                this.animateValue(counter, 0, target, this.config.animationDuration, suffix, decimal);
            }, index * 200 + 500);
        });
    },

    animateValue(element, start, end, duration, suffix = '', decimal = 0) {
        const startTime = performance.now();
        const range = end - start;
        const update = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 4);
            const current = start + (range * ease);
            element.textContent = (decimal > 0 ? current.toFixed(decimal) : Math.round(current)) + suffix;
            if (progress < 1) requestAnimationFrame(update);
            else element.textContent = (decimal > 0 ? end.toFixed(decimal) : Math.round(end)) + suffix;
        };
        requestAnimationFrame(update);
    },

    initComponentLinks() {
        const items = [
            { id: 'telegram', url: 'telegram-app.html' },
            { id: 'chatbot', url: 'telegram-app.html?openChat=true' }
        ];
        items.forEach(item => {
            const card = document.querySelector(`.component-card[data-component="${item.id}"]`);
            if (card) {
                card.style.cursor = 'pointer';
                card.onclick = () => window.location.href = item.url;
            }
        });

        const intCard = document.querySelector('.component-card[data-component="integration"]');
        if (intCard) {
            intCard.style.cursor = 'pointer';
            intCard.onclick = () => {
                document.getElementById('integration-modal').classList.add('show');
                document.body.style.overflow = 'hidden';
            };
        }
    },

    initMobileTabs() {
        const buttons = document.querySelectorAll('.tab-button');
        const columns = document.querySelectorAll('.column');
        if (!buttons.length) return;
        
        const activate = (tabName) => {
            buttons.forEach(b => b.classList.toggle('active', b.dataset.tab === tabName));
            const sectionName = tabName.replace('section-', '');
            columns.forEach(c => {
                if (window.innerWidth < 1024) {
                    c.style.display = c.dataset.section === sectionName ? 'block' : 'none';
                } else {
                    c.style.display = 'block';
                }
            });
        };
        
        buttons.forEach(b => b.onclick = () => activate(b.dataset.tab));
        
        if (window.innerWidth < 1024) {
            const activeButton = document.querySelector('.tab-button.active');
            if (activeButton) {
                activate(activeButton.dataset.tab);
            }
        }
        
        window.onresize = () => {
            if (window.innerWidth >= 1024) {
                columns.forEach(c => c.style.display = 'block');
            } else {
                const activeButton = document.querySelector('.tab-button.active');
                if (activeButton) {
                    activate(activeButton.dataset.tab);
                }
            }
        };
    },

    initTableInteraction() {
        const rows = document.querySelectorAll('#comparison-table tbody tr');
        rows.forEach(row => {
            row.onmouseenter = () => row.classList.add('highlighted');
            row.onmouseleave = () => row.classList.remove('highlighted');
        });
    },

    initTimelineInteraction() {
        // Timeline is handled by direct onclick in HTML for reliability
    },

    initScrollAnimations() {
        const obs = new IntersectionObserver((entries) => {
            entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('is-visible'); });
        });
        document.querySelectorAll('.animate-on-scroll').forEach(el => obs.observe(el));
    }
};

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
