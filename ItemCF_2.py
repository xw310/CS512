#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
movie recommendation system for CS512
'''
import numpy as np
import random
import copy
import sys
from load_moviename import *

script, log  = sys.argv
f = open(log,'w')
__con__ = sys.stderr
sys.stderr = f

class ItemCF():

    def __init__(self):
        self.train_set = {}
        self.test_set = {}
        self.pivot = 0.7

        self.recommend_number = 10
        self.similar_number = 20

        self.sim_dic = {}
        self.user_aver_rate = {}

        print ('initialization complete',file = sys.stderr)

    def load_file(self,dataset):
        f1 = open(dataset,'r')
        for i, dataline in enumerate(f1):
            yield  dataline

            if i% 1000 == 0:
                print(f'{i} lines has been loaded',file = sys.stderr)

        f1.close()
        print('loading complete',file = sys.stderr)

    def train_and_test(self,dataset):
        train_count = 0
        test_count = 0
        iter_lines = self.load_file(dataset)
        print('return', iter_lines,file = sys.stderr)
        for line in iter_lines:
            user, movie, ratings, _ = line.split('::')
            #print(line)
            if random.random() < self.pivot:
                self.train_set.setdefault(user,{})
                self.train_set[user][movie] = ratings
                train_count += 1

            else:
                self.test_set.setdefault(user,{})
                self.test_set[user][movie] = ratings
                test_count += 1

        print(f'partition of trainset and test set complete, number of trainset {train_count}, number of testset {test_count}',file = sys.stderr)
        #print(self.train_set,file = sys.stderr)#####################################
        #print('***************************',file = sys.stderr)######################
        #print(self.test_set,file = sys.stderr)#################################
        #print('***************************',file = sys.stderr)######################

    def calculate_sim(self):
        for user, value in self.train_set.items():
            count = 0
            sum = 0
            self.user_aver_rate.setdefault(user)
            for movie, rate in value.items():
                count += 1
                sum += int(rate)
            #print(count,file = sys.stderr)#######################
            self.user_aver_rate[user] = sum/count
        #print(self.user_aver_rate)

            #print(self.user_aver_rate,file = sys.stderr)##################33
        #a = input()########################3

        sim_denominator = {}
        for user, value in self.train_set.items():
            for movie,rate in value.items():
                if movie not in sim_denominator:
                    sim_denominator.setdefault(movie)
                    sim_denominator[movie] = 1
                    #print(user,movie,rate,(float(rate) - self.user_aver_rate[user])**2,sim_denominator[movie])
                    #a=input()
                    if sim_denominator[movie] == 0:
                        sim_denominator[movie] += 0.00000001   #in case denominator = 0
                else:
                    sim_denominator[movie] += 1
                    #print(user,movie,rate,(float(rate) - self.user_aver_rate[user])**2,sim_denominator[movie])
                    #a=input()
        #print(sim_denominator)

        #print(sim_denominator,'qwer',file = sys.stderr)
        #a=input()

        for user, value in self.train_set.items():
            for movie1,rate1 in value.items():
                #print(movie1,rate1,file = sys.stderr)   #############
                self.sim_dic.setdefault(movie1,{})
                for movie2,rate2 in value.items():
                    #print(movie2,rate2,file = sys.stderr)###########
                    if movie1 == movie2:
                        #a = input('cal第二部分循环，相等跳过')##########################
                        pass

                    else:
                        if movie2 not in self.sim_dic[movie1]:
                            #a = input('cal第二部分循环，不相等第一次')##########################
                            self.sim_dic[movie1].setdefault(movie2,[])
                            ###p1 = (float(rate1) - self.user_aver_rate[user])**2
                            ###p2 = (float(rate2) - self.user_aver_rate[user])**2
                            p0 = 1
                            self.sim_dic[movie1][movie2].append(p0)
                            ###self.sim_dic[movie1][movie2].append(p1)
                            ###self.sim_dic[movie1][movie2].append(p2)
                            #print(self.sim_dic,file = sys.stderr)#############################
                            #a=input()#############################

                        else:
                            #print(self.sim_dic[movie1][movie2])#############################
                            #a=input('cal第二部分循环,不相等第二次')#############################
                            ###p1 = (float(rate1) - self.user_aver_rate[user])**2
                            ###p2 = (float(rate2) - self.user_aver_rate[user])**2
                            p0 = 1
                            self.sim_dic[movie1][movie2][0] += p0
                            ##self.sim_dic[movie1][movie2][1] += p1
                            ##self.sim_dic[movie1][movie2][2] += p2
                            #print(self.sim_dic[movie1][movie2])#############################
                            #print(self.sim_dic,file = sys.stderr)##############################
                            #a=input()####################################
        #print(self.sim_dic)
        #sim
        for movie1 in self.sim_dic:
            for movie2, p in self.sim_dic[movie1].items():
                p3 = p[0]/(sim_denominator[movie1]**0.5*sim_denominator[movie2]**0.5)
                #print(p,file = sys.stderr)######################################
                #a = input()#####################
                # situation of division by 0!!!
                #p3 = p[0] / ((p[1]**0.5)*(p[2]**0.5))
                p.clear()
                p.append(p3)
        #print(self.sim_dic,file = sys.stderr)##############################
        print('calculation of similarity dictionary complete',file = sys.stderr)
        #a=input()

    def recommending(self, user):
        R = self.recommend_number
        S = self.similar_number
        #print(self.train_set,file = sys.stderr)##############################
        #a = input()################################
        user_watched = self.train_set[user]
        #print(user_watched,file = sys.stderr)##############################
        #a = input('开始推荐')##########################
        recommendation = {}

        for movie, rating in user_watched.items():
            if movie not in self.sim_dic:
                print(f'movie {movie} is not in database',file = sys.stderr)

            else:
                #print(self.sim_dic[movie].items())
                list = sorted(self.sim_dic[movie].items(), key=lambda x:x[1][0], reverse=True)
                list = list[:S]

                #print(movie,'corresponding list',list,file = sys.stderr)##############################
                #a = input('相思电影list')##########################
                for sim_movie, similarity in list:
                    if sim_movie in user_watched:
                        #print('看过',file = sys.stderr)##############################
                        #a = input('看过')##########################
                        pass

                    else:
                        if sim_movie not in recommendation:
                            recommendation.setdefault(sim_movie,[])
                            p0 = similarity[0] * float(rating)
                            recommendation[sim_movie].append(p0)
                            recommendation[sim_movie].append(abs(similarity[0]))
                            #print('第一次循环',recommendation,file = sys.stderr)##########################
                            #a = input('第一次循环')########################
                        else:
                            p0 = similarity[0] * float(rating)
                            recommendation[sim_movie][0] += p0
                            recommendation[sim_movie][1] += abs(similarity[0])

        #print('recommend',recommendation,file = sys.stderr)##############################
        #a = input('recommendation')##########################

        for movie,p in recommendation.items():
            #p2 = p[0] / p[1]
            p2 = p[0]
            p.clear()
            p.append(p2)

        rec_list = sorted(recommendation.items(), key=lambda x:x[1][0], reverse=True)[:R]

        #for elem in rec_list:
            #print(f'recommendations:{elem}\n',file = sys.stderr)###################################
        #a = input('reclist is shown in file')#######################################
        return rec_list

    def estimation(self):
        hit = 0
        R = self.recommend_number

        rec_total = 0
        test_total = 0

        for i, user in enumerate(self.train_set):
            rec_list = self.recommending(user)
            test_movies = self.test_set.get(user,{})
            #print(test_movies,'******')
            #print(rec_list,'#######')
            for movie, _ in rec_list:
                if movie in test_movies:
                    hit += 1

            rec_total += R
            test_total += len(test_movies)
            print(f'第{i}个user')
            print('hit',hit,'rec_total',rec_total,'test_total',test_total)
            #a=input()

        precision = hit / rec_total

        recall = hit / test_total
        print(f'prscision is {precision} and recall is {recall}',file = sys.stderr)###################################
        #a = input('results shown in file')#######################################

if __name__ == '__main__':

    rating_data = 'ml-1m/ratings.dat'
    itemcf = ItemCF()
    itemcf.train_and_test(rating_data)
    itemcf.calculate_sim()
    #itemcf.recommending('1')
    itemcf.estimation()
    movie_data = 'ml-1m/movies.dat'
    l_MN = load_MovieName()
    l_MN.load_file(movie_data)
    #print(len(l_MN.MovieName))

    while(True):
        s1 = input('If you want to experience this system? Input y to experience and n to quit ')
        print('\n')
        #print(s1,type(s1))
        if s1!='y' and s1!= 'n':
            print('error input; choose again')
            continue

        if s1 == 'n':
            break

        if s1 == 'y':
            user = input('please input your name: ')
            itemcf.train_set.setdefault(user,{})
            while(True):
                print('Input the movie you once watched and ratings.')
                movie = input('movie name: ')
                ratings = input('ratings for the movie above: ')
                itemcf.train_set[user][movie] = ratings
                s2 = input('if over, input c to cease; if not, press any key to continue   ')
                print('\n')
                if s2 == 'c':
                    #flag = 0
                    break
                else:
                    pass

        print('###########################',file = sys.stderr)###################################
        recommendation_list = itemcf.recommending(user)

        for elem in recommendation_list:
            index = l_MN.MovieName.index(elem[0])
            print(elem[0],'   ', end=' ',file = sys.stderr)
            print(l_MN.MovieName[index+1],'   ', end=' ',file = sys.stderr)
            print(l_MN.MovieName[index+2],'   ', end=' ',file = sys.stderr)
            print(elem[1],'\n',file = sys.stderr)
