
  cordova.define('cordova/plugin_list', function(require, exports, module) {
    module.exports = [
      {
          "id": "cordova-plugin-ionic.common",
          "file": "plugins/cordova-plugin-ionic/dist/common.js",
          "pluginId": "cordova-plugin-ionic",
        "clobbers": [
          "IonicCordova"
        ]
        },
      {
          "id": "cordova-plugin-ionic.guards",
          "file": "plugins/cordova-plugin-ionic/dist/guards.js",
          "pluginId": "cordova-plugin-ionic",
        "runs": true
        }
    ];
    module.exports.metadata =
    // TOP OF METADATA
    {
      "cordova-plugin-ionic": "5.4.7",
      "cordova-plugin-whitelist": "1.3.4"
    };
    // BOTTOM OF METADATA
    });
    