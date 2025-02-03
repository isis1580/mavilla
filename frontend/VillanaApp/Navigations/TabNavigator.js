import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { FontAwesome } from '@expo/vector-icons';
import { BlurView } from 'expo-blur';
import { useNavigation } from '@react-navigation/native';
import Accueil from '../components/Accueil';
import NotificationScreen from '../components/NotificationScreen'; 
import CameraScreen from '../components/CameraScreen'; 
import MessageScreen from '../components/MessageScreen'; 
import MenuScreen from '../components/MenuScreen';
import { StyleSheet,TouchableOpacity,Text } from 'react-native';
import { Actionsheet, Box } from 'native-base';
const Tab = createBottomTabNavigator();

const CustomTabBar = () => {
  const navigation = useNavigation();

  return (
    <BlurView intensity={20} tint="default" style={styles.bottomMenu}>
      <TouchableOpacity style={styles.menuButton} onPress={() => navigation.navigate("Accueil")}>
        <FontAwesome name="home" size={22} color="#fff" />
        <Text style={styles.iconText}>Home</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.menuButton} onPress={() => navigation.navigate("Notifications")}>
        <FontAwesome name="bell-o" size={22} color="#fff" />
        <Text style={styles.iconText}>Notifications</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.cameraButton} onPress={() => navigation.navigate("Camera")}>
        <FontAwesome name="camera" size={40} color='#6ab6cc' />
      </TouchableOpacity>

      <TouchableOpacity style={styles.menuButton} onPress={() => navigation.navigate("Messages")}>
        <FontAwesome name="envelope-o" size={22} color="#fff" />
        <Text style={styles.iconText}>Messages</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.menuButton} onPress={() => navigation.navigate("Menu")}>
        <FontAwesome name="bars" size={22} color="#fff" />
        <Text style={styles.iconText}>Menu</Text>
      </TouchableOpacity>
    </BlurView>
  );
};

const TabNavigator = () => {
  return (
    <Tab.Navigator tabBar={props => <CustomTabBar {...props} />} screenOptions={{ headerShown: false }}>
      <Tab.Screen name="Accueil" component={Accueil} />
      <Tab.Screen name="Notifications" component={NotificationScreen} />
      <Tab.Screen name="Camera" component={CameraScreen} />
      <Tab.Screen name="Messages" component={MessageScreen} />
      <Tab.Screen name="Menu" component={MenuScreen} />
    </Tab.Navigator>
  );
};

const styles = StyleSheet.create({
  bottomMenu: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: 'rgba(0,0,0,0.2)',
    padding: 15,
  },
  menuButton: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  iconText: {
    fontSize: 12,
    color: '#fff',
  },
  cameraButton: {
    alignItems: 'center',
    top:-8

  },

    villana: {
        height: 600,
        width: 150,
        justifyContent: 'center',
        alignItems: 'center',
        resizeMode: 'contain',
        marginBottom: 5,
    },

    searchButton: {
      margin: 'auto',
      marginHorizontal: 5 ,      
    },


});

export default TabNavigator;