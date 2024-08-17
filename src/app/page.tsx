"use client"
import Image from "next/image";
import { useState } from 'react';
import { IntelligentReport } from './IntelligentReport'
import { HealthReadingsUI} from './HealthReadingsUI'
import { NoteFhir } from "./NoteFhir";
import Link from "next/link"
import { cn } from "@/src/lib/utils"
import {
  NavigationMenu,

  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,

  navigationMenuTriggerStyle,
} from "@/src/ui/navigation-menu"

export default function Home() {

  const menuItems = [
    { name: 'Medi Mind', href: '', tab: 'intelligent-report', component: <IntelligentReport/> },
    { name: 'Blue Pulse', href: '', tab: 'health-readings', component: <HealthReadingsUI/> },
    { name: 'Note 2 FHIR', href: '', tab: 'note-fhir', component: <NoteFhir/> }
    // Add more menu items as needed
  ];

  const [activeMenuItem, setActiveMenuItem] = useState(menuItems[0])
  const renderContent = () => (activeMenuItem as any).component;


    return (
        <div className="container">
            <NavigationMenu>
              <NavigationMenuList>
                {menuItems.map((item, index) => (
                  <NavigationMenuItem key={index}>
                    <Link href={item.href} legacyBehavior passHref>
                      <NavigationMenuLink
                        className={navigationMenuTriggerStyle()}
                        onClick={() => setActiveMenuItem(item as any)}
                      >
                        {item.name}
                      </NavigationMenuLink>
                    </Link>
                  </NavigationMenuItem>
                ))}
              </NavigationMenuList>
            </NavigationMenu>
            <div className="content">
                {renderContent()}
            </div> 
        </div>
    );

}

