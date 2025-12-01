import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import TabNavigator from '../Navigations/TabNavigator';
import MaisonList from '../components/MaisonList';
import HotelsDetails from '../components/HotelsDetails';
import TextoScreen from '../components/TextoScreen';
import SearchScreen from '../components/SearchScreen'
import ProfilScreen from '../components/ProfileScreen'
import LoginScreen from '../components/loginscreen';
import UserForm from '../components/UserForm';


const Stack = createStackNavigator();


const MainNavigator = () => {
  return (
    
      <NavigationContainer>
        <Stack.Navigator initialRouteName="TabNavigator">
          <Stack.Screen 
            name="TabNavigator" 
            component={TabNavigator} 
            options={{ headerShown: false ,
              
            }} 
          />
          <Stack.Screen 
            name="Maison" 
            component={MaisonList} 
            options={{ headerShown: false,
              gestureEnabled: true,
             }} 
            
          />
          <Stack.Screen 
            name="HotelsDetails" 
            component={HotelsDetails} 
            options={{ 
              headerShown: false,
              gestureEnabled: true,
    
            }} 
            
          />
          <Stack.Screen 
            name="Search" 
            component={SearchScreen} 
            options={{ 
              headerShown: false,
              gestureEnabled: true,
    
            }} 
            
          />
          <Stack.Screen 
            name="ProfilScreen" 
            component={ProfilScreen} 
            options={{ 
              headerShown: false,
    
            }} 
            
          />
          <Stack.Screen 
            name="LoginScreen" 
            component={LoginScreen} 
            options={{ 
              headerShown: false,
    
            }} 
            
          />
          <Stack.Screen 
            name="UserForm" 
            component={UserForm} 
            options={{ 
              headerShown: false,
    
            }} 
            
          />
          <Stack.Screen 
            name="TextoScreen" 
            component={TextoScreen} 
            options={{ headerShown: false,
              gestureEnabled: true,
             }} 
            
          />
        </Stack.Navigator>
      </NavigationContainer>
    
  );
}

export default MainNavigator;