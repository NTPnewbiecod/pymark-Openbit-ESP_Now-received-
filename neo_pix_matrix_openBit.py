import machine
import neopixel


class led_matrix_MAIN():
  
  def __init__(self):
    self.neopixel_matrix = neopixel.NeoPixel(machine.Pin(13), 25, bpp=3, timing=2)
  
  def hex_color(self, hex_vals:str):
    """ "ffffff" -> (255,255,255)

    Args:
        hex_vals (str): _description_ 
    Returns:
        _type_: _description_
    """
    hex_vals = list(hex_vals)
    _almost_out_val = [0] *3
    temp_ver = [''] *2
    _out_index = 0
    for index_here , val in enumerate(hex_vals):
        if index_here % 2 == 0:
            temp_ver[index_here % 2] = str(val)
            temp_ver[index_here % 2 +1] = str(val)
            _almost_out_val[_out_index] = ''.join(temp_ver)
            _out_index += 1
            
            
            def base16_to_int(a):
                return int(a, 16)
            
            result = map(base16_to_int, _almost_out_val)
            
            
    
    return tuple(result)
  
  def led_matrix_active(self):
    """init and send color data to neopixel matrix. to put it simply, this function just make neopixel light up 
    """
    self.neopixel_matrix.write()     
        
  def led_matrix_fill(self, color: tuple):
        """load color value into memory

        Args:
            color (tuple): tuple that contain RGB (int between 0 to 255) eg. (255, 255, 255)
        """
        self.neopixel_matrix.fill(color)
  
  # def 