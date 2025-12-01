import React, { useState } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
const MenuScreen = () => {
  const navigation = useNavigation();
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  const menuItems = [

    { id: '2', title: 'Aide et Assistance' },
    { id: '3', title: 'Confidentialité' },
    { id: '4', title: 'Accès Professionnel' },
    { id: '5', title: 'Paramètres' },
    { id: '6', title: 'Déconnexion' },
    { id: '7', title: 'Archives' },
    { id: '8', title: 'À Propos' },
    { id: '9', title: 'Faire un Don' },
  ];

  const renderPair = ({ item }) => (
    <View style={styles.pairContainer}>
      {item[0] && (
        <TouchableOpacity style={styles.menuItem} onPress={() => console.log(`${item[0].title} Pressed`)}>
          <Text style={styles.menuItemText}>{item[0].title}</Text>
        </TouchableOpacity>
      )}
      {item[1] && (
        <TouchableOpacity style={styles.menuItem} onPress={() => console.log(`${item[1].title} Pressed`)}>
          <Text style={styles.menuItemText}>{item[1].title}</Text>
        </TouchableOpacity>
      )}
    </View>
  );

  // Regrouper les éléments en paires
  const pairedMenuItems = [];
  for (let i = 0; i < menuItems.length; i += 2) {
    pairedMenuItems.push(menuItems.slice(i, i + 2));
  }

  return (
    <View style={[styles.container, isDarkMode ? styles.darkContainer : styles.lightContainer]}>
      <View style={styles.header}>
        <View style={styles.profileContainer}>
        
          <TouchableOpacity onPress={() => navigation.navigate('ProfilScreen')}>          
              <Image source={require('../assets/profil.jpg')} style={styles.profileImage}
          
            />
          </TouchableOpacity>
          <Text style={styles.userName}>Isis</Text>
        </View>
        <TouchableOpacity onPress={toggleTheme} style={styles.themeToggle}>
          <Ionicons name={isDarkMode ?  'moon' : 'sunny'} size={24} color={isDarkMode ?  '#444' : '#FFD700'} />
        </TouchableOpacity>
      </View>
      <FlatList
        data={pairedMenuItems}
        renderItem={renderPair}
        keyExtractor={(item, index) => index.toString()}
        contentContainerStyle={styles.menuList}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
rkContainer: {
    backgroundColor: '#333',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
    marginTop: 50,
    borderTopLeftRadius:30,
    borderTopRightRadius:30,
    backgroundColor:'#95a5a6',
    marginHorizontal:10,
  },
  profileContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  profileImage: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginRight: 10,
    resizeMode:'cover',
    borderWidth:1,
    borderColor:'#fff',
  },
  userName: {
    fontSize: 20,
    fontWeight: 'bold',
    color:'#fff'
  },
  themeToggle: {
    marginLeft: 20,
  },
  menuList: {
    padding: 10,
  },
  pairContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  menuItem: {
    backgroundColor: '#fff', // Couleur de fond légèrement bleue
    borderRadius: 15,
    width: 180,
    height: 100,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 5, // Espacement horizontal entre les éléments
  },
  menuItemText: {
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#444', // Changer la couleur du texte en blanc
  },
});

export default MenuScreen;