import React, { useState } from 'react';
import { View, Text, StyleSheet, FlatList, Pressable, Image } from 'react-native';
import { SwipeListView } from 'react-native-swipe-list-view';
import { Entypo, MaterialIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

const MessageScreen = () => {
  const initialData = [
    {
      id: '1',
      fullName: 'Nass',
      timeStamp: '12:47 PM',
      recentText: 'Bonjour suis interesse!',
      avatarUrl: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
    },
    {
      id: '2',
      fullName: 'Mamie',
      timeStamp: '11:11 PM',
      recentText: 'On peut se voir ?',
      avatarUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyEaZqT3fHeNrPGcnjLLX1v_W4mvBlgpwxnA&usqp=CAU'
    },
    {
      id: '3',
      fullName: 'abdoul',
      timeStamp: '6:22 PM',
      recentText: 'D"accord bien recu!',
      avatarUrl: 'https://miro.medium.com/max/1400/0*0fClPmIScV5pTLoE.jpg'
    },
    {
      id: '4',
      fullName: 'Oumar',
      timeStamp: '8:56 PM',
      recentText: 'Hello bro',
      avatarUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr01zI37DYuR8bMV5exWQBSw28C1v_71CAh8d7GP1mplcmTgQA6Q66Oo--QedAN1B4E1k&usqp=CAU'
    },
  ];
  const navigation = useNavigation();
  const [listData, setListData] = useState(initialData);

  const deleteRow = (rowKey) => {
    const newData = listData.filter(item => item.id !== rowKey);
    setListData(newData);
  };

  const renderItem = ({ item }) => (
    <Pressable style={styles.rowFront} onPress={() => navigation.navigate('TextoScreen', { 
      userName: item.fullName, // Passer le nom complet
      avatarUrl: item.avatarUrl // Passer l'URL de l'avatar
    })}>
      <View style={styles.rowContent}>
        <Image  source={require('../assets/profil.jpg')} style={styles.avatar} />
        <View style={styles.textContainer}>
          <Text style={styles.name}>{item.fullName}</Text>
          <Text style={styles.message}>{item.recentText}</Text>
        </View>
        <Text style={styles.timeStamp}>{item.timeStamp}</Text>
      </View>
    </Pressable>
  );

  const renderHiddenItem = (data) => (
    <View style={styles.rowBack}>
      <Pressable style={[styles.backRightBtn, styles.backRightBtnLeft]} onPress={() => console.log('More')}>
        <Entypo name="dots-three-horizontal" size={24} color="black" />
      </Pressable>
      <Pressable style={[styles.backRightBtn, styles.backRightBtnRight]} onPress={() => deleteRow(data.item.id)}>
        <MaterialIcons name="delete" size={24} color="white" />
      </Pressable>
    </View>
  );

  return (
    <View style={styles.container}>
     <View style={styles.viewtitle}>
      <Text style={styles.title}>Messages</Text>
    </View>
      <SwipeListView
        data={listData}
        renderItem={renderItem}
        renderHiddenItem={renderHiddenItem}
        rightOpenValue={-130}
        previewRowKey={'1'}
        previewOpenValue={-40}
        previewOpenDelay={3000}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 10,
  },
  title: {
    marginTop: 50,
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
    
    
  },
  viewtitle:{

    justifyContent:'center',
    alignItems:'center',
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  
  
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
    marginRight: 10,
    resizeMode:'cover',
    borderWidth:1,
    borderColor:'grey',
  },
  textContainer: {
    flex: 1,
  },
  name: {
    fontWeight: 'bold',
    fontSize: 16,
  },
  message: {
    color: '#666',
    fontSize: 14,
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
    justifyContent: 'space-between',
    paddingLeft: 15,
  },
  backRightBtn: {
    alignItems: 'center',
    bottom: 0,
    justifyContent: 'center',
    position: 'absolute',
    top: 0,
    width: 75,
  },
  backRightBtnLeft: {
    backgroundColor: '#CCC',
    right: 75,
  },
  backRightBtnRight: {
    backgroundColor: 'red',
    right: 0,
  },
});

export default MessageScreen;
