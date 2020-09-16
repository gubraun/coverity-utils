#include <stdio.h>
#include <string.h>

int main()
{

	char *hello = "Hello World\n";

	/* size of this buffer ok for 64b arch, but
     * too small for 32b archs */
	char out_s[2*sizeof(long)];

	memcpy(out_s, hello, strlen(hello));

	printf("%s", out_s);

	return 0;
}
