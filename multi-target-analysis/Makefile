archs := armv8-a armv7-r x86 x86_64
objs := $(foreach arch,$(archs),$(arch)/hello.o)

all: dirs $(objs)

armv8-a/hello.o: hello.c
	aarch64-linux-gnu-gcc -march=armv8-a -o $@ -c $<
#	arm-none-eabi-gcc --specs=nosys.specs -march=armv8-a -o $@ -c $<

armv7-r/hello.o: hello.c
	arm-none-eabi-gcc --specs=nosys.specs -march=armv7-r -o $@ -c $<

x86/hello.o: hello.c
	gcc -m32 -o $@ $<

x86_64/hello.o: hello.c
	gcc -m64 -o $@ $<

dirs:
	mkdir -p $(archs)

clean:
	rm -rf $(archs)

.PHONY: dirs clean
