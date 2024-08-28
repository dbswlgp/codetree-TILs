from collections import deque

N,M,K = map(int,input().split())

array = []

turret = 0
for i in range(N):
  array.append(list(map(int,input().split())))
  for j in range(M):
    if array[i][j] > 0:
      turret += 1

attack_time = [[0]*M for _ in range(N)]
this_time = 1

def attacker(array):
  attacker_i = 0
  attacker_j = 0
  power = 5001
  for i in range(N):
    for j in range(M):
      if array[i][j] != 0:
        if array[i][j] < power:
          power = array[i][j]
          attack_can = [[i,j]]
        elif array[i][j] == power:
          attack_can.append([i,j])
  if len(attack_can) >= 2:
    time = -1
    for can in attack_can:
      if attack_time[can[0]][can[1]] > time:
        time = attack_time[can[0]][can[1]]
        attack_can2 = [can]
      elif attack_time[can[0]][can[1]] == time:
        attack_can2.append(can)
    if len(attack_can2) >= 2:
      rc = -1
      for can in attack_can2:
        if can[0] + can[1] > rc:
          rc = can[0] + can[1]
          attack_can3 = [can]
        elif can[0] + can[1] == rc:
          attack_can3.append(can)
      if len(attack_can3) >= 2:
        attack_can3.sort(key=lambda x:x[1], reverse=True)
      attacker_i = attack_can3[0][0]
      attacker_j = attack_can3[0][1]
    else:
      attacker_i = attack_can2[0][0]
      attacker_j = attack_can2[0][1]
  else:
    attacker_i = attack_can[0][0]
    attacker_j = attack_can[0][1]

  array[attacker_i][attacker_j] += (N+M)
  global this_time
  attack_time[attacker_i][attacker_j] = this_time
  this_time += 1

  return attacker_i, attacker_j

def attacked(array,attacker_i,attacker_j):
  attacked_i = 0
  attacked_j = 0
  power = 0
  for i in range(N):
    for j in range(M):
      if array[i][j] != 0 and (i!=attacker_i or j!=attacker_j):
        if array[i][j] > power:
          power = array[i][j]
          attack_can = [[i,j]]
        elif array[i][j] == power:
          attack_can.append([i,j])
  if len(attack_can) >= 2:
    time = 1001
    for can in attack_can:
      if attack_time[can[0]][can[1]] < time:
        time = attack_time[can[0]][can[1]]
        attack_can2 = [can]
      elif attack_time[can[0]][can[1]] == time:
        attack_can2.append(can)
    if len(attack_can2) >= 2:
      rc = 21
      for can in attack_can2:
        if can[0] + can[1] < rc:
          rc = can[0] + can[1]
          attack_can3 = [can]
        elif can[0] + can[1] == rc:
          attack_can3.append(can)
      if len(attack_can3) >= 2:
        attack_can3.sort(key=lambda x:x[1])
      attacked_i = attack_can3[0][0]
      attacked_j = attack_can3[0][1]
    else:
      attacked_i = attack_can2[0][0]
      attacked_j = attack_can2[0][1]
  else:
    attacked_i = attack_can[0][0]
    attacked_j = attack_can[0][1]

  return attacked_i, attacked_j

def razer(attacker_i,attacker_j,attacked_i,attacked_j):
  global turret
  attack_visited = [[False]*M for _ in range(N)]
  attack_visited[attacker_i][attacker_j] = True
  dx = [0,1,0,-1]
  dy = [1,0,-1,0]
  visited = [[False]*M for _ in range(N)]
  q = deque([[attacker_i,attacker_j,[]]])
  visited[attacker_i][attacker_j] = True
  while q:
    x,y,route = q.popleft()
    if x == attacked_i and y == attacked_j:
      for i,j in route:
        if i == attacked_i and j == attacked_j:
          if array[i][j] > array[attacker_i][attacker_j]:
            array[i][j] -= array[attacker_i][attacker_j]
          else:
            array[i][j] = 0
            turret -= 1
        else:
          if array[i][j] > (array[attacker_i][attacker_j]//2):
            array[i][j] -= (array[attacker_i][attacker_j]//2)
          else:
            array[i][j] = 0
            turret -= 1
        attack_visited[i][j] = True
      for i in range(N):
        for j in range(M):
          if attack_visited[i][j] == False and array[i][j] != 0:
            array[i][j] += 1
      return True
    for t in range(4):
      nx = x + dx[t]
      ny = y + dy[t]
      if nx<0:
        nx = N-1
      if nx>=N:
        nx = 0
      if ny<0:
        ny = M-1
      if ny>=M:
        ny = 0
      if array[nx][ny] != 0 and visited[nx][ny] == False:
        visited[nx][ny] = True
        q.append([nx,ny,route+[[nx,ny]]])
        
  return False

def shell(attacker_i,attacker_j,attacked_i,attacked_j):
  global turret
  visited = [[False]*M for _ in range(N)]
  visited[attacker_i][attacker_j] = True
  dx = [0,1,1,1,0,-1,-1,-1]
  dy = [1,1,0,-1,-1,-1,0,1]
  if array[attacked_i][attacked_j] > array[attacker_i][attacker_j]:
    array[attacked_i][attacked_j] -= array[attacker_i][attacker_j]
  else:
    array[attacked_i][attacked_j] = 0
    turret -= 1
  visited[attacked_i][attacked_j] = True
  for t in range(8):
    nx = attacked_i + dx[t]
    ny = attacked_j + dy[t]
    if nx<0:
      nx = N-1
    if nx>=N:
      nx = 0
    if ny<0:
      ny = M-1
    if ny>=M:
      ny = 0
    if array[nx][ny] != 0 and (nx!=attacker_i or ny!=attacker_j):
      if array[nx][ny] > (array[attacker_i][attacker_j]//2):
        array[nx][ny] -= (array[attacker_i][attacker_j]//2)
      else:
        array[nx][ny] = 0
        turret -= 1
      visited[nx][ny] = True
  for i in range(N):
    for j in range(M):
      if visited[i][j] == False and array[i][j] != 0:
        array[i][j] += 1

for _ in range(K):
  attacker_i,attacker_j = attacker(array)
  attacked_i,attacked_j = attacked(array,attacker_i,attacker_j)
  if not razer(attacker_i,attacker_j,attacked_i,attacked_j):
    shell(attacker_i,attacker_j,attacked_i,attacked_j)
  if turret == 1:
    break


powerful = 0
for i in range(N):
  for j in range(M):
    powerful = max(powerful,array[i][j])

print(powerful)