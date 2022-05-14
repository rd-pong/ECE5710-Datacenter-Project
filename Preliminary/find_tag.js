"use strict";

// First the usual required imports
var Cylon = require("cylon");
var path = require("path");

// Get the IPs of the drones we are working with from the script arguments
var drones_ip = [
                //  "192.168.1.22",
                //  "192.168.1.23",
                //  "192.168.1.25",
                 "192.168.1.1"];

// Land on ctrl-Z (I'm fairly sure this does NOT work)
process.on('SIGTSTP', function() {
  robots.forEach(function (robot, index, array) {
    robot.devices.drone.land;
    robot.devices.drone.stop;
  });
  console.log("stopping all!");
});

// Set up the robots array that will contain all the robots we will control:
var robot = null,
robots = [];

// Now it is time for the actual work:
drones_ip.forEach(function (val, index, array) {
  robot = Cylon.robot({
    name: ("AR Parrot Drone at " + val),
    connections: {
      ardrone: { adaptor: "ardrone", port: val },
    },

    devices: {
      drone: { driver: "ardrone", connection: "ardrone" },
      nav: { driver: "ardrone-nav", connection: "ardrone" },
    },

    work: function(my) {
      my.drone.config("general:navdata_demo", "TRUE");

      // Select the active tag detection
      my.drone.config('detect:detect_type', 10);  // 10 = CAD_TYPE_MULTIPLE_DETECTION_MODE,  The drone uses several detections at the same time

      //The color of the hulls you want to detect. Possible values are green, yellow and blue (respective integer values as of 2.1/1.10 firmware : 1, 2, 3).
      my.drone.config('detect:enemy_colors', 3);

      // Bitfields to select detections that should be enabled on horizontal camera.
      my.drone.config('detect:detections_select_v_hsync', 128);

      // Bitfields to select detections that should be enabled on horizontal camera.
      my.drone.config('detect:detections_select_h', 32);

      var from = new Date();
      var to = 0;
      my.nav.on("navdata", function(data){

        if (data.visionDetect) {
          to = new Date();
            if (data.visionDetect.nbDetected > 0 && (to - from > 5000)) {
              console.log("detected");
              after((0).seconds(), my.drone.land);
              after((0).seconds(), my.drone.stop);
            }
        }
      });
      my.drone.takeoff();
      //my.drone.clockwise(360);
    }
  });

  // We now add this new robot to the list of current robots
  robots.push(robot);
});

// Now we simply start every robot!
console.log("Starting all robots.....");
robots.forEach(function (robot, index, array) {
  robot.start();
});
