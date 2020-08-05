import subprocess

while True:
    p = subprocess.Popen(['python', 'test_case.py'])
    #(output, err) = p.communicate()
    p_status = p.wait()
    print('condition met')
    print(p_status)
    break
