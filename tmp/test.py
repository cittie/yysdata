import xlsxwriter

string = "R8bb1ac44bp_us|1.0582|0,Pqbad4575oj_us||0,YJbb0e9ffJz_us|1.1119|0,zAbb0a154Ro_us|0.799646|0,Dxbadb26aZl_us||0,80bb17273B1_us|1.0854|0,hxbb0cee2Rt_us|1.0434|0,6Sbb18bbeNc_us|1.20797|0,W4baf1a19Fl_us||0,z1bb2ac11rP_us||0,hWbae0856Vd_us||0,8jbb20e7820_us||0,Gdbaf0181ud_us||0,0Dbb18b0aqE_us|1.06569|0,6zbb0be70s0_us||0,cFbb2004cRm_us||0,Lobb11e2cqD_us||0,JObb2602f1w_us||0,Z9bb0a0b1Ot_us||0,jFbb158ebjf_us||0"
result = []
s = string.split('|')
size = len(s)

for i in range(size >> 1):
    if not s[i * 2 + 1]:
        s[i * 2 + 1] = '0'
    result.append(s[i * 2] + '/t' + s[i * 2 + 1] + '/n')

print(result)