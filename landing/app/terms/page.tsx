import type { Metadata } from "next";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = {
  title: "Terms of use — pulse",
  description:
    "Terms applying to the local pulse app (free tier). Pro and Team tiers have their own service agreement when they ship.",
  alternates: { canonical: "/terms" },
  openGraph: {
    title: "Terms of use — pulse",
    description: "MIT-licensed local app · use without warranty · trademark info.",
    url: "https://mintforai.com/terms",
    type: "article",
  },
};

export default function TermsPage() {
  return (
    <LegalPage
      title="Terms of use"
      subtitle="These terms apply to the local pulse app (free tier). Pro and Team tiers will have their own service agreement when they ship."
      lastUpdated="2026-05-12"
    >
      <h2>License (free tier)</h2>
      <p>
        Pulse is provided <strong>as-is</strong>, free of charge, for personal and internal business
        use. The local app is open source under{" "}
        <a href="https://github.com/walight999/pulse/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">MIT License</a>. You may:
      </p>
      <ul>
        <li>Run pulse on as many of your own machines as you want</li>
        <li>Modify the source code for personal use</li>
        <li>Export your data at any time (CSV / .ics)</li>
        <li>Fork and redistribute the code under MIT terms</li>
      </ul>
      <p>You may not:</p>
      <ul>
        <li>Use the "pulse" name or wordmark in derivative products without permission</li>
        <li>Remove the "pulse" attribution in exports unless you've forked the code</li>
        <li>Claim affiliation with or endorsement by the pulse project without permission</li>
      </ul>

      <h2>No warranty</h2>
      <p>
        Pulse is provided without warranty of any kind. The authors are not liable for any damages
        arising from use of the software, including but not limited to:
      </p>
      <ul>
        <li>Lost or corrupted data</li>
        <li>Missed subscription renewals</li>
        <li>Inaccurate cost calculations</li>
        <li>Compatibility issues with your operating system</li>
      </ul>
      <p>
        You are responsible for keeping your own backups (pulse auto-backs up but isn't a
        substitute for off-machine storage).
      </p>

      <h2>Third-party services</h2>
      <p>Pulse uses:</p>
      <ul>
        <li><strong>frankfurter.dev</strong> — exchange rates (free, no key)</li>
        <li><strong>Anthropic Admin API</strong> — only if you provide your own key</li>
      </ul>
      <p>These services have their own terms. Pulse is not affiliated with them.</p>

      <h2>Updates</h2>
      <p>
        Pulse may release updates that change features or behavior. You are not required to install
        updates, but unsupported versions may stop working correctly with newer data files or
        third-party services.
      </p>

      <h2>Trademarks</h2>
      <p>
        "pulse" and the pulse logo are trademarks of the project. Other names mentioned in the app
        (Anthropic, Claude, Cursor, OpenAI, Gemini, etc.) are trademarks of their respective owners.
      </p>

      <h2>Changes to these terms</h2>
      <p>
        These terms may be updated. Material changes will be announced in the release notes.
        Continued use after an update constitutes acceptance.
      </p>

      <h2>Governing law</h2>
      <p>
        To be specified at the Pro launch. For now, no specific jurisdiction applies; use is at your
        own discretion.
      </p>

      <h2>Contact</h2>
      <p>
        Questions:{" "}
        <a href="https://github.com/walight999/pulse/issues" target="_blank" rel="noopener noreferrer">
          open an issue on the repository
        </a>{" "}
        or email <a href="mailto:hi@mintforai.com">hi@mintforai.com</a>.
      </p>
    </LegalPage>
  );
}
