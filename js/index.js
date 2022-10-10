
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[type="radio"]').forEach((e) => {
        e.addEventListener('change', (f) => {
            var selected = f.target.id;
            if (selected === 'optWifi') {
                document.querySelector('#wifi-setup').style.display = 'block';
            } else {
                document.querySelector('#wifi-setup').style.display = 'none';
            }
        })
    })
});