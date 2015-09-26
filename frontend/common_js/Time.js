var strftime = require('strftime');

var Time = {
    human: function (timestamp) {

        var current = parseInt(Date.now() / 1000);

        var delta = current - timestamp;

        if (delta < 30){
            return 'epp most';
        }
        if (delta < 60){
            return 'fel perce';
        }
        if (delta < 120){
            return 'egy perce';
        }
        if (delta < 3600){
            return '' + parseInt(delta/60) + ' perce';
        }
        if (delta < 86400){
            return '' + parseInt(delta/3600) + ' oraja';
        }
        if (delta < (86400*2)){
            return 'tegnap';
        }
        if (delta < (86400*3)){
            return 'tegnapelott';
        }
        if (delta < (86400*6)){
            return '' + parseInt(delta/3600/24) + ' napja';
        }
        return strftime('%B %d.', new Date(timestamp));
    }
};
module.exports = Time