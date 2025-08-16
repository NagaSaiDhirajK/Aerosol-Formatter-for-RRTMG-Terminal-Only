#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def main():
    import numpy as np

    def one_digit_format(val, rng):
        return val[-1:] if val.isdigit() and (int(val) in range(rng+1)) else 'NaN'

    def two_digits_format(val):
        return ('0' + val) if val.isdigit() and len(val) == 1 else (val[-2:] if val.isdigit() else 'NaN')
    
    def two_digits_format_without_0(val):
        return val if val.isdigit() and (len(val) in range(4) and int(val)/100 < 0) else (val[-2:] if val.isdigit() else 'NaN')

    NAER = two_digits_format(NAER := input('Enter Record A1.1 Number of Aerosols (1-99)'))[-1:]

    def _format_line(values, widths):
        out = [f"{v:>{widths[i]}}" if widths and i < len(widths) else v for i, v in enumerate(values)]
        return "".join(out)

    def _float_fmt(values, float_fmt):
        out = [format(v, float_fmt) if isinstance(v, float) and float_fmt else str(v) for i, v in enumerate(values)]
        return "".join(out)

    def is_float(val):
        try:
            float(val)
            return True
        except ValueError:
            return False

    def _float_digit(val, float_fmt, rng):
        return format(float(val), float_fmt) if is_float(val) and (0.0 <= float(val) <= float(rng)) else 'NaN'

    output = []
    for i in range(int(NAER)):
        ind_aer_output = []
        NLAY = two_digits_format(NLAY := input('Enter Record A2.1 Number of Layers w/ Aerosols(0-51)'))
        IOAD = one_digit_format(IOAD := input('Enter Record A2.1 Aerosol Depth w/ AERPAR or Ind. IB (0-1)'), 1) 
        ISSA = one_digit_format(ISSA := input('Enter Record A2.1 Aerosol SSA Gray or Ind. IB (0-1)'), 1) 
        IPHA = one_digit_format(IPHA := input('Enter Record A2.1 Aerosol Phase Gray or Ind. IB (0-2)'), 2)
        ind_aer_output.append([_format_line(list(NLAY), [4]), _format_line(list(IOAD), [5]), _format_line(list(ISSA), [5]), _format_line(list(IPHA), [5])])

        if any(v == 'NaN' for v in [NLAY, IOAD, ISSA, IPHA]):
            print('Invalid inputs')
            break
        
        aerosol_ioad_layer = []
        if int(IOAD) == 0:
            AERPAR1 = _float_digit(AERPAR1 := input('Enter Record A2.1 Aerosol Optical Depth Parameters AERPAR1(0.00-1.00)'), '1.2f', 1)
            AERPAR2 = _float_digit(AERPAR2 := input('Enter Record A2.1 Aerosol Optical Depth Parameters AERPAR2(0.00-1.00)'), '1.2f', 1)
            AERPAR3 = _float_digit(AERPAR3 := input('Enter Record A2.1 Aerosol Optical Depth Parameters AERPAR3(0.00-1.00)'), '1.2f', 1)
            ind_aer_output.append([_format_line(list(AERPAR1), [5]),_format_line(list(AERPAR2), [5]),_format_line(list(AERPAR3), [5])])
            for j in range(int(NLAY)):
                Aer_layer_in = input(f'Enter Record A2.1.1 Aerosol Layer for Optical Depth @ 1 μm (0-51) #{j}')
                Aer_layer = two_digits_format_without_0(Aer_layer_in)
                Aer_IOAD_in = input(f'Enter Record A2.1.1 Aerosol Layer Optical Depth (0.0000-1.0000) #{j}')
                Aer_IOAD = _float_digit(Aer_IOAD_in, '1.4f', 1) + '0'
                aerosol_ioad_layer.append([
                    _format_line(list(Aer_layer), [5]) if len(str(_format_line(list(Aer_layer), [5]))) == 5 
                    else (_format_line(list(Aer_layer), [4]) if len(str(_format_line(list(Aer_layer), [4]))) == 5 
                    else _format_line(list(Aer_layer), [3])),
                    Aer_IOAD
                ])
            ind_aer_output.append(aerosol_ioad_layer)  
        else:
            ind_aer_output.append([_format_line(list('0.00'), [5]),_format_line(list('0.00'), [5]),_format_line(list('0.00'), [5])])
            for j in range(int(NLAY)):
                Aer_layer_in = input(f'Enter Record A2.1.1 Aerosol Layer for Optical Depth @ 1 μm (0-51) #{j}')
                Aer_layer = two_digits_format_without_0(Aer_layer_in)
                aer_temp = [_format_line(list(Aer_layer), [5]) if len(str(_format_line(list(Aer_layer), [5]))) == 5 
                            else (_format_line(list(Aer_layer), [4]) if len(str(_format_line(list(Aer_layer), [4]))) == 5 
                            else _format_line(list(Aer_layer), [3]))]
                for k in range(14):
                    Aer_IOAD_in = input(f'Enter Record A2.1.1 Aerosol Layer Optical Depth (0.0000-1.0000) #{j}')
                    Aer_IOAD = _float_digit(Aer_IOAD_in, '1.4f', 1) + '0'
                    aer_temp.append(Aer_IOAD)
                aerosol_ioad_layer.insert(0, aer_temp)
            ind_aer_output.append(aerosol_ioad_layer)

        aer_temp_2 = []
        if int(ISSA) == 0:
            IB16_ISSA = _float_digit(IB16_ISSA := input('Enter Record A2.2 SSA for First Band IB16 (0.00-1.00)'), '1.2f', 1) + '0'
            ind_aer_output.append([IB16_ISSA])
        else:
            for k in range(14):
                IB_ISSA_in = input('Enter Record A2.2 SSA for Bands IB16-29 (0.00-1.00)')
                IB_ISSA = _float_digit(IB_ISSA_in, '1.2f', 1) + '0'
                aer_temp_2.append(IB_ISSA)
            ind_aer_output.append(aer_temp_2)

        aer_temp_3 = []
        if int(IPHA) == 0:
            IB16_IPHA = _float_digit(IB16_IPHA := input('Enter Record A2.1/A2.3 Asymmetry Param. for First Band IB16 (0.00-1.00)'), '1.2f', 1) + '0'
            ind_aer_output.append([IB16_IPHA])
        else:
            for k in range(14):
                IB_IPHA_in = input('Enter Record A2.1/A2.3 Asymmetry Param. for Bands IB16-29 (0.00-1.00)')
                IB_IPHA = _float_digit(IB_IPHA_in, '1.2f', 1) + '0'
                aer_temp_3.append(IB_IPHA)
            ind_aer_output.append(aer_temp_3)

        output.append(ind_aer_output)

    NAER_format = _format_line(list(NAER), [5]) if len(str(_format_line(list(NAER), [5]))) == 5 else _format_line(list(NAER), [4]) 
    output.insert(0, [NAER_format])

    with open('Aer_input.txt', 'w') as f:
        for i, item in enumerate(output):
            if i > 0:
                f.write(''.join(item[0] + item[1]) + '\n')
                for sub in item[2:]:
                    if isinstance(sub[0], list):
                        for sub2 in sub:
                            f.write(''.join(sub2) + '\n')
                    else:
                        f.write(''.join(sub) + '\n')
            elif isinstance(item, list):
                f.write(''.join(item) + '\n')
            else:
                f.write(str(item) + '\n')
                
if __name__ == "__main__":
    main()


# In[ ]:




