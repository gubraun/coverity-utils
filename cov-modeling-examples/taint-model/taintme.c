/* functions that deliver untrusted data */

/* foo is being modeled... */
int foo();

/* ... and bar uses code annotations */

// coverity[ +taint_source ]
int bar()
{
	int ret = 0;
	return ret;
}


int main()
{
	int buf[8] = {0};
	int n = foo(); /* get untrusted data */
	int k = bar(); /* get untrusted data */

	return buf[n] + buf[k]; /* uh-uh */
}

