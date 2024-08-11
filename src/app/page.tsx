"use client"
import Image from "next/image";
import { useState } from 'react';
import { IntelligentReport } from './IntelligentReport'
import { HealthReadingsUI} from './HealthReadingsUI'
import Link from "next/link"
import { cn } from "@/lib/utils"
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"
export default function Home() {

    const [activeTab, setActiveTab] = useState('')

    const renderContent = () => {
        switch (activeTab) {
            case 'health-readings':
                return <HealthReadingsUI />;
            case 'intelligent-report':
                return <IntelligentReport />;
        }
    };


    return (
        <div className="container">
            {/* <nav className="tabs">
            <button onClick={() => setActiveTab('intelligent-report')}>Medi Mind</button>
                <button >Blue Pulse</button>
            </nav>
           */}
            <NavigationMenu>
              <NavigationMenuList>
              <NavigationMenuItem>
                  <Link href=""  legacyBehavior passHref>
                    <NavigationMenuLink className={navigationMenuTriggerStyle()} onClick={() => setActiveTab('intelligent-report')} >
                    Medi Mind
                    </NavigationMenuLink>
                  </Link>
                </NavigationMenuItem>
                <NavigationMenuItem>
                  <Link href="" legacyBehavior passHref>
                    <NavigationMenuLink className={navigationMenuTriggerStyle()} onClick={() => setActiveTab('health-readings')} >
                      Blue Pulse
                    </NavigationMenuLink>
                  </Link>
                </NavigationMenuItem>
              </NavigationMenuList>
            </NavigationMenu>
            <div className="content">
                {renderContent()}
            </div> 
        </div>
    );

}

