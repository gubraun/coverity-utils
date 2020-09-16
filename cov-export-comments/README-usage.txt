
Example command line usage:

C:\Python27\python.exe cov-extract-triage-comments.py --config cov-extract-triage-comments.config --cusername <USENAME> --cpassword <PASSWORD> --sensible 500 --cstream <STREAM_NAME> --mode 0x80 --output <FILENAME>.csv

======================================================================================

You could filter all defects/issues where this custom attribute is defined somewhere

--custom Mitigation:Approved

custom = Mitigation:Approved

Or if more than one value

--custom Mitigation:Approved,Proposed

custom = Mitigation:Approved,Proposed


This filtering only works for custom attributes though.  It NPEs with built in attributes

run with --debug 4 to see these values being unpacked and utilized in the query

======================================================================================

Installing Python 2.7 with SOAP support from scratch
----------------------------------------------------
Start with the Windows or Linux install from here:  https://www.python.org/downloads/release/python-279/

Update pip and setuptools from the distribution:  
	\Python27\Scripts\pip.exe install --upgrade pip                  (Python installer)
	\Python27\Scripts\pip.exe install --upgrade setuptools           (setup, dependencies tool)

Then add autopep8, python-ntlm, suds-jurko, pylint and prospector:
	\Python27\Scripts\pip.exe install --upgrade autopep8             (smart indenter)  
	\Python27\Scripts\pip.exe install --upgrade python-ntlm          (Windows NT Domain auth)  
	\Python27\Scripts\pip.exe install --upgrade suds-jurko           (SOAP lib)  
	\Python27\Scripts\pip.exe install --upgrade pylint               (Lint for Python)  
	\Python27\Scripts\pip.exe install --upgrade prospector           (static analysis for Python)

