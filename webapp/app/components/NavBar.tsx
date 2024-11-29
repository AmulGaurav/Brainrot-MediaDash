"use client";

import { useRouter } from "next/navigation";
import SearchBar from "./SearchBar";
import { SignedIn } from "@clerk/nextjs";
import Link from "next/link";
import { SignOutButton } from "@clerk/nextjs";
import PopoverComponent from "./PopoverComponent";

export default function AppBar() {
  const router = useRouter();

  return (
    <SignedIn>
      <div className="px-4 md:px-6 lg:px-9 2xl:px-10 flex justify-between items-center p-3">
        <button
          className="px-3 py-1.5 text-white font-semibold bg-red-600 hover:bg-red-700 rounded-lg"
          onClick={() => {
            router.push("/");
          }}
        >
          MediaDash
        </button>

        <div>
          <SearchBar />
        </div>

        <Link
          href="/dashboard"
          className="hidden lg:block mt-1 px-5 py-2.5 rounded-full bg-[#131316] hover:bg-gray-900 text-white font-semibold"
        >
          Dashboard
        </Link>

        <div className="hidden lg:block">
          <SignOutButton>
            <button className="px-3 py-1.5 bg-blue-800 hover:bg-blue-700 font-semibold text-white rounded-lg">
              Sign out
            </button>
          </SignOutButton>
        </div>

        <div className="hidden md:block lg:hidden w-16 h-[41px] px-4 py-2 bg-white rounded-2xl">
          <PopoverComponent />
        </div>
      </div>
    </SignedIn>
  );
}