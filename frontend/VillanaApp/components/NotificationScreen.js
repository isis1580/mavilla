import React, { useState } from 'react';
import { View, Text, StyleSheet, FlatList, Pressable, Image } from 'react-native';
import { Entypo, MaterialIcons } from '@expo/vector-icons';

const NotificationScreen = () => {
  const initialData = [
    {
      id: '1',
      title: 'Nouvelle demande ',
      timeStamp: '12:47 PM',
      avatarUrl: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
    },
    {
      id: '2',
      title: 'Message de Moussa',
      timeStamp: '11:11 PM',
      avatarUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyEaZqT3fHeNrPGcnjLLX1v_W4mvBlgpwxnA&usqp=CAU'
    },
    {
      id: '3',
      title: 'Karim a aimé votre publication',
      timeStamp: '6:22 PM',
      avatarUrl: 'https://miro.medium.com/max/1400/0*0fClPmIScV5pTLoE.jpg'
    },
    {
      id: '4',
      title: 'Hassana a commenté votre photo',
      timeStamp: '8:56 PM',
      avatarUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr01zI37DYuR8bMV5exWQBSw28C1v_71CAh8d7GP1mplcmTgQA6Q66Oo--QedAN1B4E1k&usqp=CAU'
    },
    {
      id: '5',
      title: 'Nouvelle mise à jour disponible',
      timeStamp: '5:30 PM',
      avatarUrl: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
    },
    {
      id: '6',
      title: 'Vous avez reçu un nouveau message',
      timeStamp: '4:15 PM',
      avatarUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyEaZqT3fHeNrPGcnjLLX1v_W4mvBlgpwxnA&usqp=CAU'
    },
    {
      id: '7',
      title: 'Rappel: Rdv à 3 PM',
      timeStamp: '3:00 PM',
      avatarUrl: 'https://miro.medium.com/max/1400/0*0fClPmIScV5pTLoE.jpg'
    },
    {
      id: '8',
      title: 'Votre abonnement a été renouvelé',
      timeStamp: '2:45 PM',
      avatarUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr01zI37DYuR8bMV5exWQBSw28C1v_71CAh8d7GP1mplcmTgQA6Q66Oo--QedAN1B4E1k&usqp=CAU'
    },
    {
      id: '9',
      title: 'Nouvelle fonctionnalité ajoutée',
      timeStamp: '1:30 PM',
      avatarUrl: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
    },
    {
      id: '10',
      title: 'Vous avez été tagué dans une photo',
      timeStamp: '12:00 PM',
      avatarUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyEaZqT3fHeNrPGcnjLLX1v_W4mvBlgpwxnA&usqp=CAU'
    },
  ];

  const [listData, setListData] = useState(initialData);

  const deleteNotification = (id) => {
    const newData = listData.filter(item => item.id !== id);
    setListData(newData);
  };

  const renderItem = ({ item }) => (
    <Pressable style={styles.rowFront} onPress={() => console.log('Notification Pressed')}>
    <View style={styles.rowContent}>
      <Image  source={require('../assets/profil.jpg')} style={styles.avatar} />
      <View style={styles.textContainer}>
        <Text style={styles.title}>{item.title}</Text>
        <Text style={styles.timeStamp}>{item.timeStamp}</Text>
      </View>
    </View>
  </Pressable>
);

const renderHiddenItem = (data) => (
  <View style={styles.rowBack}>
    <Pressable style={[styles.backRightBtn, styles.backRightBtnRight]} onPress={() => deleteNotification(data.item.id)}>
      <MaterialIcons name="delete" size={24} color="white" />
    </Pressable>
  </View>
);

return (
  <View style={styles.container}>
    <View style={styles.viewtitle}>
      <Text style={styles.titletop}>Notifications</Text>
    </View>
    <FlatList
      data={listData}
      renderItem={renderItem}
      keyExtractor={item => item.id}
      showsVerticalScrollIndicator={false}
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.listContainer}
    />
  </View>
);
};

const styles = StyleSheet.create({
container: {
  flex: 1,
  backgroundColor: '#fff',
  padding: 10,

  flexDirection:'column'
},
viewtitle:{

  justifyContent:'center',
  alignItems:'center',
  marginTop: 50,
  borderBottomWidth: 1,
  borderBottomColor: '#ccc',


},
titletop: {
  fontSize: 24,
  fontWeight: 'bold',
  marginBottom: 10,
  
},
rowFront: {
  backgroundColor: '#fff',
  paddingVertical: 15,
  paddingHorizontal: 10,
},
rowContent: {
  flexDirection: 'row',
  alignItems: 'center',
  
},
avatar: {
  width: 50,
  height: 50,
  borderRadius: 25,
  borderWidth:1,
  borderColor:'grey',
  marginRight: 10,
  resizeMode:'cover'
},
textContainer: {
  flex: 1,
},
title: {
  fontWeight: 'bold',
  fontSize: 16,
},
timeStamp: {
  color: '#999',
  fontSize: 12,
},
rowBack: {
  alignItems: 'center',
  backgroundColor: '#DDD',
  flex: 1,
  flexDirection: 'row',
  justifyContent: 'flex-end',
  paddingLeft: 15,
},
backRightBtn: {
  alignItems: 'center',
  justifyContent: 'center',
  width: 75,
},
backRightBtnRight: {
  backgroundColor: 'red',
  right: 0,
},
});

export default NotificationScreen;