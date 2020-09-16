#include <string.h>

//void my_memcpy(void*, const void*, size_t);
void my_memcpy(void *d, const void *s, size_t n)
{
    unsigned int i;

    for (i = 0; i < n; ++i) {
	((char*)d)[i] = ((char*)s)[i];
    }
    //__coverity_writeall__(d);
}


int main()
{   
    char dst[4];
    const char *src = "Hello World";

    my_memcpy(dst, src, 8);

    return 0;
}
