import network
import espnow



def just_split(string0: str, separator: str):
  return str(string0).split(':')
    
def raw_text_addr_to_bytes(addr_in):
  """'ff:ff:ff:ff:ff:ff' to bytes([255,255,255,255,255,255])

  Args:
      addr_in (bytes): ____
  """
  _addr = just_split(addr_in, ":")
  for index, val in enumerate(_addr):
    _addr[index] = int(str(val), 16)
  return bytes(_addr)
    


class ESPN ():
  def __init__(self) -> None:
    
    #network driver setup
    self._net_wlan = network.WLAN(network.STA_IF)  # Or network.AP_IF | I don't know?
    self._net_wlan.active(True)
    self._net_wlan.disconnect()

    #ESPNow set up
    self._EspNow = espnow.ESPNow()
    self._EspNow.__init__() #just in case
    self._EspNow.active(True)

    #default value
    self._sender_address :bytes = b'\x00' * 6
    self._recv_msg :bytes= "default_msg".encode("utf-8")
    
  
  def _DEBUG_peer_count(self) -> None:
    peer_count_and_encrypt = self._EspNow.peer_count()
    print(f'total peer {peer_count_and_encrypt[0]}\nencrypt peer: {peer_count_and_encrypt[1]}')

  def _get_peer_count(self) -> tuple:
    """Return the number of registered peers:

    Returns:
        tuple:(peer_num, encrypt_num): where peer_num is the number of peers which are registered, 
        and encrypt_num is the number of encrypted peers.
    """
    peer_count_and_encrypt = self._EspNow.peer_count()
    return peer_count_and_encrypt

  def _get_peers(self) -> tuple:
    """Return information on a registered peer

    Returns:
        tuple: tuple tuple with info on all registered peer
    """
    return self._EspNow.get_peers()
  
  def _print_peers_info(self):
    """print information on all registered peer.
    """
    for i in  self._get_peers():
      mac, lmk, channel, ifdix, is_encrypt = i
      mac = ":".join("%02X" % i for i in mac)
      # lmk = "".join( str(i) for i in lmk)
      if ifdix == 0:
        ifdix_name = "network.STA_IF"
      else:
        ifdix_name = "network.AP_IF"
      print(f'mac:          {mac}')
      print(f'LMK key:      {lmk}')
      print(f'wifi channel: {channel}')
      print(f'ifdix:        {ifdix_name}')
      print(f'is_encrypt:   {is_encrypt}')
  
  
  def addPeer(self, addr_in :str, channel :int= 0,) -> None:
    """Add/register the provided mac address as a peer. 

    Args:
        ADDR (str): The MAC address of the peer (such as "FF:FF:FF:FF:FF:FF")
        Channel (int, optional): The wifi channel (2.4GHz) to communicate with this peer. 
        Must be an integer from 0 to 14. 
        If channel is set to 0 the current channel of the wifi device will be used. Defaults to 0.

    
    """
    
    try:
      self._EspNow.add_peer(raw_text_addr_to_bytes(addr_in), b'', channel)
    except OSError as err:
      if err.args[1] == "ESP_ERR_ESPNOW_FULL":
        print("\n\n!!! too many peers are already registered. !!! \n\n")
        raise err
      else:
        pass


  def send(self, msg :str, MAC_of_recv:str= None) ->None:
    """Send the data contained in "msg" to the peer with given network MAC address.
    if MAC address is not provided. this function will send the "msg" to all MAC address that is already register.
    !!!The peer MUST be registered with ESPNow.add_peer() before the message can be sent.

    Args:
        msg (str): string or byte-string up to espnow.MAX_DATA_LEN (250) bytes long.
        MAC_of_recv (str, optional): The MAC address of the receiver (such as "FF:FF:FF:FF:FF:FF"). Defaults to None.
    """
    if MAC_of_recv == None:
      self._EspNow.send(bytearray(msg,'utf-8'))
    else:
      try:
        # self._EspNow.send(msg.encode("utf-8"), mac=raw_text_addr_to_bytes(MAC_of_recv))
        self._EspNow.send(raw_text_addr_to_bytes(MAC_of_recv), bytearray(msg,'utf-8'))
      except OSError as err:
        print("Sending error !\nSomething goes wrong when sending msg")
        raise err
    
  
  
  def _isReadyToRead(self) -> bool:
    """Check if data is available to be read with readAsText/readAsNumber method.

    Returns:
        bool:
    """
    self._sender_address, self._recv_msg = self._EspNow.irecv(10)
    if self._recv_msg:
      return True
    else:
      return False
  
  def getSenderMAC(self) -> str:
    """Return the MAC address of the latest message.

    Returns:
        str: in the plain hex string. (such as "FF:FF:FF:FF:FF:FF")
    """
    sender_address_text :str = ""
    sender_address_text :str = ":".join("%02X" % i for i in self._sender_address)
    return sender_address_text

  def readAsText(self) -> str:
    if self._isReadyToRead():
      return self._recv_msg.decode("utf-8") if self._recv_msg else ""
    else:
      return None
  
  def readAsNumber(self) -> float:
    if self._isReadyToRead():
      if not self._recv_msg:
        return 0
      else:
          return float(self._recv_msg)
    else:
      return None
    
  def getMyMAC(self):
    return ":".join("%02X" % i for i in self._net_wlan.config('mac'))