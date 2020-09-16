#include <cstdlib>

#define SC_REPORT_FATAL(msg) \
    special_abort(msg);

void special_abort(const char *msg)
{
}

void test()
{
    int *p = (int *)malloc(16);
    *p = 0;

    SC_REPORT_FATAL("done");
}

#ifdef __COVERITY__
faildf';kasd
ab
#endif


int main()
{
    test();
    return 0;
}
