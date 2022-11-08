// document.addEventListener('DOMContentLoaded', () => {
//     document.querySelectorAll('input[type="radio"]').forEach((e) => {
//         e.addEventListener('change', (f) => {
//             var selected = f.target.id;
//             if (selected === 'optWifi') {
//                 document.querySelector('#wifi-setup').style.display = 'block';
//                 document.querySelector('#wifiSSID').focus();
//             } else {
//                 document.querySelector('#wifi-setup').style.display = 'none';
//                 document.querySelector('#accountEmail').focus();
//             }
//         })
//     })
// });

async function encodeScript() {
    const data = {
        use_wifi: document.querySelector('#optWifi').checked,
        email: document.querySelector('#accountEmail').value,
        password: document.querySelector('#accountPassword').value,
        dump_system: document.querySelector('#getSysInfo').checked
    }
    const response = await (await fetch('/encode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })).json();
    document.querySelector('#downloadLink').href = response['file'];
    document.querySelector('#duckyScript').value = response['duckycode'];
}