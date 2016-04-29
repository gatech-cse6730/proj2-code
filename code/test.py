# Parameters:
# nt, r , k
# initial amount of food available
# initial amount of power available

n_t = 20.0 # could be selected randomly
r = 2.8 # could be selected randomly
k = 500 # could be selected randomly

data = []

for i in xrange(100):
    n_tplus1 = (r * (1-(n_t/k)) * n_t)
    n_t = n_tplus1
    data.append(n_t)

plt.plot(data)
plt.show()


# In[2]:

person = Person(2, 42, 'm')
person2 = Person(6, 400, 'f')
sim_time = 100

print(person.kcal_requirements(sim_time))
print(person2.kcal_requirements(sim_time))

population = Population([person, person2], 4.0)
print(population.kcal_requirements(sim_time))


# In[3]:

facility = Facility(20000, 20)


# In[9]:

person = Person(2, 42, 'm')
person2 = Person(6, 400, 'f')
sim_time = 100
population = Population([person, person2], 4.0)
food = Food(facility, population, sim_time)
sim_time += 1
food.calculate_food_production(sim_time)