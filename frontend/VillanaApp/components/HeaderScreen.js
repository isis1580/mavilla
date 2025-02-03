import { StyleSheet, Text, View,Image, TouchableOpacity } from 'react-native'
import React, { useEffect, useState } from 'react';
import { FontAwesome } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

const HeaderScreen = () => {
    const navigation = useNavigation();
    const [userImage, setUserImage] = useState('https://example.com/user.jpg');

    
   
    return (
      <View style={styles.TopContainer}>
        <View style={styles.TopContainerchild1}>
          <Image source={require('../assets/viconcol.png')}
           
            style={styles.villana}
          />
        </View>
          
        <View style={styles.TopContainerchild2}>
  
          <TouchableOpacity style={styles.userImage} onPress={() => navigation.navigate('Search')}>
            <FontAwesome name="search" size={24} color="#444" />
          </TouchableOpacity>
  
          <TouchableOpacity style={styles.userImage} onPress={() => navigation.navigate('ProfilScreen')}>          
              <Image source={require('../assets/profil.jpg')}style={styles.user}
            />
          </TouchableOpacity> 
          <TouchableOpacity style={styles.userImage} onPress={() => navigation.navigate('LoginScreen')} >          
              <Image source={require('../assets/niger.png')}style={styles.user}
            />
          </TouchableOpacity>    
  
          
         </View>
  
         
      </View>
    );
  };

export default HeaderScreen

const styles = StyleSheet.create({


    TopContainer: {
        marginTop: 50,
        height: 60,
        justifyContent: 'space-between',
        alignItems: 'center',
        flexDirection: 'row',
    
        
      },
      TopContainerchild2: {
      
        flexDirection: 'row',
        justifyContent: 'space-between'
    
      },
      
      user: {
        width: 40,
        height: 40,
        resizeMode:'cover',
        borderRadius: 50,
        backgroundColor: '#e3e9ee',
        borderWidth: 2,
        borderColor: '#FFF',
        alignItems: 'center',
        justifyContent: 'center',
      },
      userImage: {
        width: 40,
        height: 40,
        borderRadius: 50,
        backgroundColor: '#e3e9ee',
        borderWidth: 2,
        marginRight: 5,
        borderColor: '#FFF',
        alignItems: 'center',
        justifyContent: 'center',
      },
      villana: {
        height: 600,
        width: 150,
        justifyContent: 'center',
        alignItems: 'center',
        resizeMode: 'contain',
        marginBottom: 5,
    },
})