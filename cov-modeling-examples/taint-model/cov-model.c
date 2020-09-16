int foo() 
{
	int ret;
	__coverity_mark_pointee_as_tainted__(&ret, TAINT_TYPE_FILESYSTEM);
	return ret;
}
