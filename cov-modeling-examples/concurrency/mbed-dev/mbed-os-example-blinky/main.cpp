#include "mbed.h"

DigitalOut led1(LED1);

Mutex mx;

// main() runs in its own thread in the OS
// (note the calls to Thread::wait below for delays)
int main() {
    while (true) {
	mx.lock();
        led1 = !led1;
	if (!led1) {
	    return -1;
	}
        mx.unlock();
        Thread::wait(500);
    }
}

