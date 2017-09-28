import pickle

def set_lan_cpm(cur_play_mark, turn_pack, play_num):
  # In challenge mode, if a player challenges a word, the second element 
  # of the turn_pack is the flag for challenge succeeded or failed
  try:
    chal_check = pickle.loads(turn_pack)[1]
  except:
    chal_check = turn_pack[1]

  # Increase cur_play_mark by 1 if the player isn't challenged or 
  # challenge didn't succeed.
  if type(chal_check) != type(True) or not chal_check:
    # cur_play_mark shouldn't be less than play_num
    return (cur_play_mark + 1) % play_num
  else:
    return cur_play_mark