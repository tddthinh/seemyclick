const commonUI = {
    showLoading: function() {
        $('#loadingContainer').show();
    },
    hideLoading: function() {
        $('#loadingContainer').hide();
    },
    init: function() {
        $(document).ready(function() {
            $loadingContainer = $(`<div id="loadingContainer" class="loading-container h-100 w-100">
                <div class="spinner"></div>
            </div>`);
            $("body").prepend($loadingContainer);
        });
    }
};

if (typeof window !== 'undefined') {
    window.commonUI = commonUI;
}