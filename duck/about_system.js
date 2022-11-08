const SYSTEM_INFO = document.querySelector('div[id="vpd_2.0-value"]').innerText;
const CHROME_VERSION = document.querySelector('div[id="CHROME VERSION-value"]').innerText;
const NETWORK_DEVICES = JSON.parse(document.querySelector('div[id="network_devices-value"]').innerText);
const POWERWASH_COUNT = parseInt(document.querySelector('div[id="powerwash_count-value"]').innerText);
const RELEASE_BOARD = document.querySelector('div[id="CHROMEOS_RELEASE_BOARD-value"]').innerText;
const SUBMODEL_NAME = document.querySelector('div[id="platform_identity_model-value"]').innerText;

var sysinfo_keys = SYSTEM_INFO.split('"="');
var sysinfo_json = "{" + SYSTEM_INFO;
for (var i = 0; i < sysinfo_keys.length; i++) {
    sysinfo_json = sysinfo_json.replace('"="', '":"').replace('\n', ',');
}
sysinfo_json = JSON.parse((sysinfo_json.substr(0, sysinfo_json.length - 1) + "}"));

const POST_DATA = JSON.stringify({
    system_info: sysinfo_json,
    chrome_version: CHROME_VERSION,
    network_devices: NETWORK_DEVICES,
    powerwash_count: POWERWASH_COUNT,
    model_codename: RELEASE_BOARD.split('-')[0] + '.' + SUBMODEL_NAME
});

window.location.href = `http://10.10.225.53:8000/save?data=${btoa(POST_DATA)}`;