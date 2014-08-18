def enumerate2(collection):
  i = 0
  for subcollection in collection:
    j = 0
    for element in subcollection:
      yield i, j, element
      j += 1
    i += 1