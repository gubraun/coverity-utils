#include <cstdio>

void null_deref()
{
	int *x = NULL;
// coverity[var_deref_op]
	*x = 42;
// Note: cov-analyze will still report a FORWARD_NULL, but it will be set 
// to 'Intentional' by Connect upon cov-commit-defects!
}

// coverity[ +tainted_data_return ]
int get_tainted_data()
{
	int tainted = 0;
	return tainted;
}

// coverity[ +tainted_data_sink : arg-0 ]
void trust_tainted(const void* buf)
{
	// here we trust buf
}

int main()
{
	int foo;

	printf("Getting tainted data...\n");
	foo = get_tainted_data();

	printf("Using tainted data...\n");
	trust_tainted(&foo);

	return 0;
}


