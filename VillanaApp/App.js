import 'react-native-gesture-handler'; 
import React from 'react';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import MainNavigator from './Navigations/MainNavigator';
import { NativeBaseProvider, extendTheme } from 'native-base';
import { NavigationContainer } from '@react-navigation/native';

const App = () => {
  return (
    <NativeBaseProvider>
      
        <MainNavigator />
      
    </NativeBaseProvider>
  );
};

export default App;