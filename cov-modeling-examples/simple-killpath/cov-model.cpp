#nodef SC_REPORT_FATAL(msg) __sc_exit__(msg)
void __sc_exit__(const char *msg)
{
    __coverity_panic__();
}
