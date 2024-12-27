// create an empty modbus client
const ModbusRTU = require("modbus-serial");
const client = new ModbusRTU();

// open connection to a serial port
client.connectRTUBuffered("/dev/tty.usbserial-120", { baudRate: 19200, parity: 'even' }, read);

function read() {
    // read the 2 registers starting at address 5
    // on device number 1.
    client.readHoldingRegisters(1000, 3)
        .then(console.log);
}