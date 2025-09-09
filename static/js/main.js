document.addEventListener('DOMContentLoaded', function() {
    // 임시 알림만 자동으로 사라지게 함 (dismissible 클래스가 있는 것만)
    const alerts = document.querySelectorAll('.alert.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});