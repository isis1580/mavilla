import { StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';
import React from 'react';
import * as Animatable from 'react-native-animatable'
import { FontAwesome } from '@expo/vector-icons'; 

const TitlesDetails = ({trip}) => {
  return (
    <View style={styles.container}>
      
      

      <View style={styles.container2}>
        <Animatable.View   animation="fadeInUp">
          <Text style={styles.text1}>{trip.titre}</Text>
          <Text style={styles.text1}>{trip.quartier}{trip.ville}</Text>
          <Text style={styles.text2}>{trip.description}</Text>
          
        </Animatable.View>
        <View style={styles.button}>
          <View style={styles.buttonview}>
              <TouchableOpacity style={styles.button} >
                      <Text style={styles.buttonText}>Plus de details</Text>
              </TouchableOpacity>
          </View>
          <View style={styles.buttonview}>
              <TouchableOpacity style={styles.button} >
                      <Text style={styles.buttonText}>Contacter </Text>
              </TouchableOpacity>
          </View>
        </View>
      </View>

      
      <View style={styles.RightIcon}>
        <TouchableOpacity style={styles.Icon} onPress={() => navigation.navigate('ProfilScreen')}>          
          <Image source={require('../assets/profil.jpg')} style={styles.Userprofil}
          />
        </TouchableOpacity>
        <TouchableOpacity  style={styles.Icon}>
            <FontAwesome name="heart" size={27} color="red" />
        </TouchableOpacity>
        <TouchableOpacity  style={styles.Icon}>
            <FontAwesome name="share-alt" size={27} color="#fff" />
        </TouchableOpacity>
       
      </View>
    </View>
  )
}

export default TitlesDetails

const styles = StyleSheet.create({
    container:{
        position:'absolute',
        bottom:0,
        left:0,
        right:0,
        height:'45%',
        marginHorizontal:10,
        paddingLeft:10,
        flexDirection:'row',
        justifyContent:'space-between'

       },
       container2:{
        left:0,
        right:0,
        bottom:0,
        top:200

       },   

    text1:{
        fontSize:30,
        fontWeight:'bold',
        color:'#fff'

    },

    Icon:{
     
      justifyContent:'center',
      alignContent:'center',
      margin:10

    },
    text2:{
        fontSize:25,
        color:'#fff'

       
    },
    RightIcon:{
      top:50,
      alignItems:'center',
      
    },
    Userprofil:{
      width: 40,
      height: 40,
      borderRadius: 50,
      backgroundColor: '#fff',
      borderWidth: 1,
      borderColor: '#e3e9ee',


  },
  buttonText:{
    color:'#fff',
    borderRadius:15,
    backgroundColor:'orange',
    padding:5,
    marginRight:10
  },
  button:{
    flexDirection:'row',
    marginTop:10,

    
  }
})