void my_memcpy(void *d, const void *s, size_t n)
{
    unsigned int i;

    for (i = 0; i < n; ++i) {
	d[i] = s[i];
    }
    //__coverity_writeall__(d);
}
