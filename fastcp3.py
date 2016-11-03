#!/usr/bin/python
# optimize I/O speed for copying to USB drive

import shutil, sys, os, time

buffer_size = 10485760
million = 1024 * 1024

def dst_check(f):
    try:
        return os.path.getsize(f)
    except:
        return 0

def do_copy(src,dst):

    if os.path.isdir(dst) == True:
        src_base = os.path.basename(src)
        dst = dst + '/' + src_base
    else:
        sys.exit('invalid destination')

    if not os.path.isfile(src):
        sys.exit('ERROR: path')

# destination exists, skip
    dst_size = dst_check(dst)
    if dst_size > 0:
        print "Skipping", dst, '%6.2f Mb' % (dst_size/million)
        return 0
    
    t1 = time.time()
    src_size = os.path.getsize(src)

    print "Copying", src, '%6.2f Mb' % (src_size/million)
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst, buffer_size)
            fdst.flush()
            os.fsync(fdst.fileno())

    t2 = time.time()
    print '%6.2f s' %  ((t2-t1)*1.0), dst
    return src_size

def main():
    if len(sys.argv) < 3:
        sys.exit('Insufficient args')

    t0 = time.time()
    tbytes = 0
    for f in sys.argv[1:-1]:
        tbytes = tbytes + do_copy(f,sys.argv[-1])

    t99 = time.time()
    elapsed = (t99-t0) * 1.0
    print '%6.2f s' %  (elapsed), "total", '%6.2f Mb' % (tbytes/million)
    print 'I/O rate: %6.2f Mb/s' % ((tbytes/elapsed/million))
    
if __name__ == '__main__': 
    main() 

