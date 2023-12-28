// pages/index.js
import Link from 'next/link';
import Head from 'next/head';
import { Button } from 'element-react';
import 'element-theme-default';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Quant Trading Platform</title>
        <meta name="description" content="A Quantitative Trading Platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1>Welcome to the Quant Trading Platform</h1>
        <p>Start managing your quantitative trading strategies with ease.</p>

        <nav>
          <ul>
            <li>
              <Link href="/config">
                <Button type="primary">Configuration Management</Button>
              </Link>
            </li>
            <li>
              <Link href="/data">
                <Button>Data Management</Button>
              </Link>
            </li>
            <li>
              <Link href="/model">
                <Button>Model Management</Button>
              </Link>
            </li>
            <li>
              <Link href="/evaluation">
                <Button>Evaluation</Button>
              </Link>
            </li>
          </ul>
        </nav>
      </main>

      <footer>
        <p>© 2023 Quant Trading Platform. All rights reserved.</p>
      </footer>

      <style jsx>{`
        main {
          padding: 1rem;
          text-align: center;
        }
        nav ul {
          list-style: none;
          padding: 0;
        }
        nav ul li {
          display: inline;
          margin-right: 1rem;
        }
        footer {
          text-align: center;
          padding: 2rem 0;
        }
      `}</style>
    </div>
  );
}