class Toast {
    constructor() {
        this.container = null;
        this.toasts = [];
        this.init();
    }

    init() {
        if (!this.container) {
            this.container = $('<div class="c-toast-container"></div>');
            $('body').append(this.container);
        }
    }

    show(options = {}) {
        const {
            type = 'info',
            title = '',
            message = '',
            duration = 4000,
            closable = true,
            buttons = []
        } = options;

        const toast = $(`<div class="c-toast ${type}"></div>`);

        const icon = this.getIcon(type);
        
        const buttonsHtml = buttons.length > 0 ? `
            <div class="c-toast-buttons">
                ${buttons.map((btn, index) => this.createButtonHtml(btn, index)).join('')}
            </div>
        ` : '';
        
        const html = `
            <div class="c-toast-icon">${icon}</div>
            <div class="c-toast-content">
                ${title ? `<div class="c-toast-title">${this.escapeHtml(title)}</div>` : ''}
                ${message ? `<div class="c-toast-message">${this.escapeHtml(message)}</div>` : ''}
                ${buttonsHtml}
            </div>
            ${closable ? '<button class="c-toast-close" aria-label="Close">&times;</button>' : ''}
            ${duration > 0 ? '<div class="c-toast-progress"></div>' : ''}
        `;
        
        toast.html(html);
        this.container.append(toast);
        this.toasts.push(toast);

        // Register button click handlers
        if (buttons.length > 0) {
            buttons.forEach((btn, index) => {
                if (btn.onClick && typeof btn.onClick === 'function') {
                    toast.find(`[data-toast-btn="${index}"]`).on('click', (e) => {
                        e.preventDefault();
                        btn.onClick(toast, e);
                    });
                }
            });
        }

        if (closable) {
            toast.find('.c-toast-close').on('click', () => this.hide(toast));
        }

        if (duration > 0) {
            const progress = toast.find('.c-toast-progress');
            if (progress.length) {
                progress.css({
                    width: '100%',
                    transitionDuration: `${duration}ms`
                });
                setTimeout(() => {
                    progress.css('width', '0%');
                }, 10);
            }

            setTimeout(() => {
                this.hide(toast);
            }, duration);
        }

        return toast;
    }

    createButtonHtml(button, index) {
        const {
            text = 'Button',
            style = '',
            class: customClass = '',
            noDefaultClass = false,
            attribute = ''
        } = button;

        let finalClass = '';
        
        if (noDefaultClass) {
            // Only use custom classes
            finalClass = customClass;
        } else {
            // Use default classes + custom classes
            finalClass = customClass ? `c-toast-btn ${customClass}` : 'c-toast-btn';
        }

        return `
            <button 
                ${finalClass ? `class="${finalClass}"` : ''}
                data-toast-btn="${index}"
                ${style ? `style="${style}"` : ''}
                ${attribute ? attribute : ''}
            >
                ${this.escapeHtml(text)}
            </button>
        `;
    }

    hide(toast) {
        if (!toast || !toast.parent().length) return;

        toast.addClass('hiding');
        
        setTimeout(() => {
            toast.remove();
            const index = this.toasts.indexOf(toast);
            if (index > -1) {
                this.toasts.splice(index, 1);
            }
        }, 300);
    }

    success(title, message, duration) {
        return this.show({ type: 'success', title, message, duration });
    }

    error(title, message, duration) {
        return this.show({ type: 'error', title, message, duration });
    }

    warning(title, message, duration) {
        return this.show({ type: 'warning', title, message, duration });
    }

    info(title, message, duration) {
        return this.show({ type: 'info', title, message, duration });
    }

    getIcon(type) {
        const icons = {
            success: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
            error: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
            warning: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
            info: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
        };
        return icons[type] || icons.info;
    }

    escapeHtml(text) {
        return $('<div>').text(text).html();
    }

    clear() {
        this.toasts.forEach(toast => this.hide(toast));
    }
}

const toast = new Toast();

if (typeof window !== 'undefined') {
    window.toast = toast;
}
