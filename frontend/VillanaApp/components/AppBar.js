import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { Appbar } from 'react-native-paper'
import { useNavigation } from '@react-navigation/native'

const AppBar = () => {

    const navigation=useNavigation();
      
  return (
    <View style={styles.appBar}>
      <Appbar.Header style={styles.appBar}>
        <Appbar.BackAction icon="arrow-left" onPress={() => navigation.goBack()} color="#444" />
      </Appbar.Header>
    </View>
  )
}

export default AppBar

const styles = StyleSheet.create({
    container:{
        flex:1,
        position:'absolute',
        },
    appBar: {
        position: 'absolute', 
        backgroundColor: 'transparent', 
        elevation: 0, 
        top:20
        },
      
})