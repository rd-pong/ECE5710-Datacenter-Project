var net = require('net');
var i =0;
var j =0;
var size = 200;
var total = 0;
var outbound,inbound;
var buffer = Buffer.alloc(size); // var buffer = new Buffer(size);
var client = new net.Socket();
client.connect(9000, '192.168.0.22', function() {	console.log('Connected'); });

client.on('data', function(data) {
  //outbound = Date.now();
	//console.log(process.hrtime(inbound));
  total+=process.hrtime(inbound)[1];
  i++;
  if(i==1000){
    console.log(`average single trip cost after ${i} round trips sending ${size} bytes:`);
    console.log(total/i/2/1000000 + " ms");
		total =0;
		i=0;
		j++;
		if(j==10){
			client.destroy();
			return;
		}
		size *=2;
		buffer = Buffer.alloc(size);
  }
  inbound = process.hrtime();
  client.write(buffer);


});

client.on('close', function() {
	console.log('Connection closed');
});

inbound = process.hrtime();
client.write("hello");
