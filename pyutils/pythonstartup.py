import sys
if not sys.argv.count('-b'):
    print 'Loading pythonstartup.py'
    import rlcompleter, readline
    readline.parse_and_bind( 'tab: complete' )
    readline.parse_and_bind( 'set show-all-if-ambiguous On' )
