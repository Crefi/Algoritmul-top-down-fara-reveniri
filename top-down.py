
#Grammar
# E → TE′
# E′ → +TE′ | − TE′| λ
# T → FT′
# T′ → ∗ FT′ | /FT′ | λ
# F → (E)|id|num


class ParsingError(Exception):
  pass

def Alex(input_string):
  # Initialize the input string and current position
  input_string = input_string.strip()
  pos = 0
  # Define the parsing functions
  def E(pos):
    # Parse the T and E' non-terminals
    t_result, pos = T(pos)
    e_result, pos = E_Prime(pos)
    print("E -> TE'")
    return ('E',t_result, e_result), pos



  def E_Prime(pos):

    # Look ahead to the next character in the input string
    if pos < len(input_string) and input_string[pos] in ('+', '-'):
      # Consume the character and parse the T and E' non-terminals
      pos += 1
      t_result, pos = T(pos)
      e_result, pos = E_Prime(pos)
      print("E' -> {}TE'".format(input_string[pos - 1]))
      return ('E_Prime', (input_string[pos-1], t_result, e_result)), pos
    # If the next character is not + or -, then we have reached the end of the E' production,
    # and we can return
    else:
      print("E' -> epsilon")
      return ('E_Prime', None), pos


  def T(pos):
    # Parse the F and T' non-terminals
    f_result, pos = F(pos)
    t_result, pos = T_Prime(pos)
    print("T -> FT'")
    return ('T',f_result, t_result), pos

  def T_Prime(pos):
    # Look ahead to the next character in the input string
    if pos < len(input_string) and input_string[pos] in ('*', '/'):
      # Consume the character and parse the F and T' non-terminals
      pos += 1
      f_result, pos = F(pos)
      t_result, pos = T_Prime(pos)
      print("T' -> {}FT'".format(input_string[pos - 1]))
      return ('T_Prime', (input_string[pos-1], f_result, t_result)), pos
    # If the next character is not * or /, then we have reached the end of the T' production,
    # and we can return
    else:
      print("T' -> epsilon")
      return ('T_Prime', None), pos

  def F(pos):
      # Look ahead to the next character in the input string
      if pos < len(input_string) and input_string[pos] == '(':
          # Consume the character and parse the E non-terminal
          pos += 1
          result, pos = E(pos)
          # Consume the closing parenthesis
          pos += 1
          print("F -> (E)")
          return ('F', result), pos
      elif pos < len(input_string) and input_string[pos].isalpha():
          # Consume the character and return
          pos += 1
          print("F -> id")
          return ('F', input_string[pos - 1]), pos
      elif pos < len(input_string) and input_string[pos].isdigit():
          # Consume all consecutive digits
          num_str = ''
          while pos < len(input_string) and input_string[pos].isdigit():
              num_str += input_string[pos]
              pos += 1
              print("F -> num")
          return ('F', num_str), pos
      else:
          raise ParsingError('Error at position {}: unexpected character {}'.format(pos, input_string[pos]))

  result, pos = E(pos)
  if pos == len(input_string):
        return result
  else:
      raise ParsingError('Error at position {}: unexpected character {}'.format(pos, input_string[pos]))


# Parse an input string and print the result
input_string = '23*(a-b/c)+x'
try:
  result = Alex(input_string)
  print('Input string "{}" was successfully parsed!'.format(input_string))


except ParsingError as e:
    print('Parsing error: {}'.format(e))

